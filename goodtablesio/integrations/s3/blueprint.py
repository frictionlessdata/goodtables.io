import uuid
import logging

from flask import Blueprint, request, abort, jsonify
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
    return render_component('S3Settings', props={
        'userName': getattr(current_user, 'display_name', None),
    })


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


# API

# TODO:
# it should be synced with general
# approach we use for API (see api blueprint)

@s3.route('/api/bucket')
@login_required
def api_bucket_list():
    error = None
    buckets = get_user_buckets(current_user.id)
    buckets = [bucket.to_api() for bucket in buckets]
    return jsonify({
        'buckets': buckets,
        'error': error,
    })


@s3.route('/api/bucket/<bucket_name>')
@login_required
def api_bucket(bucket_name):
    try:
        code = 200
        buckets = get_user_buckets(current_user.id)
        bucket = [item for item in buckets if item.name == bucket_name][0].to_api()
        error = None
    except Exception:
        code = 404
        bucket = None
        error = 'Not Found'
    return (jsonify({
        'bucket': bucket,
        'error': error,
    }), code)


@s3.route('/api/bucket', methods=['POST'])
@login_required
def api_bucket_add():
    error = None
    payload = request.get_json()
    access_key_id = payload.get('access-key-id')
    secret_access_key = payload.get('secret-access-key')
    bucket_name = payload.get('bucket-name')

    # Check input fields
    if not access_key_id or not secret_access_key or not bucket_name:
        error = 'Missing fields'

    # Get bucket
    if not error:
        source = database['session'].query(S3Bucket).filter(
            S3Bucket.name == bucket_name).one_or_none()
        if source and source.active:
            error = 'Bucket already exists'

    # Setup bucket on aws
    if not error:
        try:
            # TODO: catch all errors inside util function
            success, message = set_up_bucket_on_aws(
                access_key_id, secret_access_key, bucket_name)
            if not success:
                error = 'Error setting up bucket integration. {0}'.format(message)
        except Exception:
            error = 'Error setting up bucket integration'

    # Create bucket in db
    if not error:
        try:
            create_bucket(
                bucket_name, access_key_id,
                secret_access_key, user=current_user)
        except Exception:
            error = 'Internal error'

    return jsonify({
        'error': error,
    })


# TODO: should we use bucket_id instead of bucket_name?
# TODO: for s3 we could have the same concept as for github - activate/deactive
@s3.route('/api/bucket/<bucket_name>/remove')
@login_required
def api_bucket_remove(bucket_name):
    error = None

    # Get bucket
    source = database['session'].query(S3Bucket).filter(
        S3Bucket.name == bucket_name).one_or_none()
    if not source:
        error = 'Unknown bucket'

    # Disable bucket on aws
    if not error:
        try:
            # TODO: catch all errors inside util function
            success, message = disable_bucket_on_aws(
                source.access_key_id, source.secret_access_key, bucket_name)
            if not success:
                error = 'Error removing bucket integration. {0}'.format(message)
        except Exception:
            error = 'Error removing bucket integration'

    # Inactivate bucket in db
    if not error:
        try:
            inactivate_bucket(bucket_name)
        except Exception:
            error = 'Internal error'

    return jsonify({
        'error': error,
    })


# Internal

def _run_validation(bucket, job_id):
    # Run validation
    tasks_chain = chain(
        get_validation_conf.s(bucket, job_id=job_id),
        validate.s(job_id=job_id))
    tasks_chain.delay()
