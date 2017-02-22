import uuid
import logging

from flask import Blueprint, flash, request, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from celery import chain

from goodtablesio import models, settings
from goodtablesio.services import database
from goodtablesio.tasks.validate import validate
from goodtablesio.utils.signature import validate_signature
from goodtablesio.utils.frontend import render_component
from goodtablesio.integrations.s3.models.bucket import S3Bucket
from goodtablesio.integrations.s3.utils import (
    set_up_bucket_on_aws, create_bucket, get_user_buckets,
    get_bucket_from_hook_payload, disable_bucket_on_aws, inactivate_bucket)
from goodtablesio.integrations.s3.tasks.jobconf import get_validation_conf

log = logging.getLogger(__name__)


s3 = Blueprint('s3', __name__, url_prefix='/s3')


@s3.record
def record_params(setup_state):
    s3.debug = setup_state.app.debug


@s3.route('/')
def index():
    jobs = models.job.get_by_integration('s3')
    return render_component('S3Home', props={
        'userName': getattr(current_user, 'display_name', None),
        'jobs': jobs,
    })


@s3.route('/settings')
@login_required
def s3_settings():
    buckets = get_user_buckets(current_user.id)
    return render_component('S3Settings', props={
        'userName': getattr(current_user, 'display_name', None),
        'buckets': [{'name': bucket.name} for bucket in buckets],
    })


@s3.route('/settings/add_bucket', methods=['POST'])
@login_required
def add_bucket():

    # Get params and validate them

    access_key_id = request.form.get('access-key-id')
    secret_access_key = request.form.get('secret-access-key')
    bucket_name = request.form.get('bucket-name')

    if not access_key_id or not secret_access_key or not bucket_name:
        flash('Missing fields', 'danger')
    else:

        source = database['session'].query(S3Bucket).filter(
            S3Bucket.name == bucket_name).one_or_none()
        if source and source.active:
            flash('Bucket already exists', 'danger')
            return redirect(url_for('s3.s3_settings'))

        success, message = set_up_bucket_on_aws(
            access_key_id, secret_access_key, bucket_name)

        # Redirect and flash message
        if success:

            conf = {'access_key_id': access_key_id,
                    'secret_access_key': secret_access_key}
            create_bucket(bucket_name, user=current_user, conf=conf)

            flash('Bucket added', 'success')
        else:
            flash('Error setting up bucket integration. {0}'.format(message),
                  'danger')

    return redirect(url_for('s3.s3_settings'))


@s3.route('/settings/remove_bucket/<bucket_name>')
@login_required
def remove_bucket(bucket_name):

    # Get params and validate them
    source = database['session'].query(S3Bucket).filter(
        S3Bucket.name == bucket_name).one_or_none()
    if not source:
        flash('Unknown bucket', 'danger')

    else:

        access_key_id = source.conf['access_key_id']
        secret_access_key = source.conf['secret_access_key']

        success, message = disable_bucket_on_aws(
            access_key_id, secret_access_key, bucket_name)

        # Redirect and flash message
        if success:

            inactivate_bucket(bucket_name)

            flash('Bucket removed', 'success')
        else:
            flash('Error removing bucket integration. {0}'.format(message),
                  'danger')

    return redirect(url_for('s3.s3_settings'))


def _run_validation(bucket, job_id):
    # Run validation
    tasks_chain = chain(
        get_validation_conf.s(bucket, job_id=job_id),
        validate.s(job_id=job_id))
    tasks_chain.delay()


@s3.route('/hook', methods=['POST'])
def create_job():

    # Validate signature
    if not s3.debug:
        key = settings.S3_LAMBDA_HOOK_SECRET
        text = request.data
        signature = request.headers.get('X-GoodTables-Signature', '')
        if not validate_signature(key, text, signature):
            msg = 'Wrong signature for AWS payload'
            log.error(msg)
            abort(400, msg)

    # Get payload parameters
    payload = request.get_json()
    if not payload:
        msg = 'No payload received'
        log.error(msg)
        abort(400, msg)

    bucket = get_bucket_from_hook_payload(payload)
    if not bucket:
        msg = 'Wrong payload received'
        log.error(msg)
        abort(400, msg)

    # Check bucket exists
    source = database['session'].query(S3Bucket).filter(
        S3Bucket.name == bucket).one_or_none()

    if not source:
        msg = ('A job was requested on a bucket not present '
               'in the DB: {}'.format(bucket))
        log.error(msg)
        abort(400, msg)

    # Save job to database
    job_id = str(uuid.uuid4())

    models.job.create({
        'id': job_id,
        'integration_name': 's3',
        'source_id': source.id,
        'conf': {
            'bucket': bucket
        }
    })

    _run_validation(bucket, job_id)

    return jsonify({'job_id': job_id})
