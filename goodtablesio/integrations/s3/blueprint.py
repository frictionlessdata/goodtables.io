import logging

from flask import Blueprint, request, abort, jsonify
from flask_login import login_required, current_user
from celery import chain

from goodtablesio import models, settings
from goodtablesio.models.base import make_uuid
from goodtablesio.services import database
from goodtablesio.tasks.validate import validate
from goodtablesio.utils.signature import validate_signature
from goodtablesio.integrations.s3.models.bucket import S3Bucket
from goodtablesio.integrations.s3.utils import (
    set_up_bucket_on_aws, create_bucket, get_user_buckets,
    get_user_buckets_count, get_bucket_from_hook_payload,
    disable_bucket_on_aws, activate_bucket, deactivate_bucket)
from goodtablesio.integrations.s3.tasks.jobconf import get_validation_conf

log = logging.getLogger(__name__)


s3 = Blueprint('s3', __name__, url_prefix='/s3')


@s3.record
def record_params(setup_state):
    s3.debug = setup_state.app.debug


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
    job_id = make_uuid()

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


@s3.route('/api/bucket/<bucket_id>')
@login_required
def api_bucket(bucket_id):
    error = None
    bucket_data = None

    # Get bucket
    try:
        bucket = (database['session'].query(S3Bucket).
                  filter(S3Bucket.users.any(id=current_user.id)).
                  filter(S3Bucket.id == bucket_id).
                  one())
        bucket_data = bucket.to_api()
    except Exception as exception:
        log.exception(exception)
        abort(403)

    return jsonify({
        'bucket': bucket_data,
        'error': error,
    })


@s3.route('/api/bucket')
@login_required
def api_bucket_list():
    error = None
    buckets = get_user_buckets(current_user.id)
    buckets_data = [bucket.to_api() for bucket in buckets]
    return jsonify({
        'buckets': buckets_data,
        'error': error,
    })


@s3.route('/api/bucket', methods=['POST'])
@login_required
def api_bucket_add():
    error = None
    bucket_data = None

    # Check current number of buckets for this user
    if not _check_number_of_buckets(current_user):
        error = 'Free plan users can only have {} active buckets'.format(
            settings.MAX_S3_BUCKETS_ON_FREE_PLAN)

    # Get input fields
    if not error:
        payload = request.get_json()
        access_key_id = payload.get('access-key-id')
        secret_access_key = payload.get('secret-access-key')
        bucket_name = payload.get('bucket-name')

        # Check input fields
        if not access_key_id or not secret_access_key or not bucket_name:
            error = 'Missing fields'

    # Get bucket
    if not error:
        bucket = database['session'].query(S3Bucket).filter(
            S3Bucket.name == bucket_name).one_or_none()
        if bucket and bucket.active:
            error = 'Bucket already exists'

    # Setup bucket on aws
    if not error:
        success, message = set_up_bucket_on_aws(
            access_key_id, secret_access_key, bucket_name)
        if not success:
            error = 'Error setting up bucket integration. {0}'.format(message)

    # Create bucket in db
    if not error:
        bucket = create_bucket(
            bucket_name, access_key_id,
            secret_access_key, user=current_user)
        bucket_data = bucket.to_api()

    return jsonify({
        'bucket': bucket_data,
        'error': error,
    })


@s3.route('/api/bucket/<bucket_id>/activate')
@login_required
def api_bucket_activate(bucket_id):
    error = None

    # Get bucket
    try:
        bucket = (database['session'].query(S3Bucket).
                  filter(S3Bucket.users.any(id=current_user.id)).
                  filter(S3Bucket.id == bucket_id).
                  one())
    except Exception as exception:
        log.exception(exception)
        abort(403)

    # Setup bucket on aws
    if not error:
        success, message = set_up_bucket_on_aws(
            bucket.access_key_id,
            bucket.secret_access_key,
            bucket.name)
        if not success:
            error = 'Error setting up bucket integration. {0}'.format(message)

    # Activate bucket in db
    if not error:
        # TODO:
        # here we have additional select query because
        # we use procedural helper instead of model helper bucket.activate()
        activate_bucket(bucket.name)

    return jsonify({
        'error': error,
    })


@s3.route('/api/bucket/<bucket_id>/deactivate')
@login_required
def api_bucket_deactivate(bucket_id):
    error = None

    # Get bucket
    try:
        bucket = (database['session'].query(S3Bucket).
                  filter(S3Bucket.users.any(id=current_user.id)).
                  filter(S3Bucket.id == bucket_id).
                  one())
    except Exception as exception:
        log.exception(exception)
        abort(403)

    # Disable bucket on aws
    if not error:
        success, message = disable_bucket_on_aws(
            bucket.access_key_id,
            bucket.secret_access_key,
            bucket.name)
        if not success:
            error = 'Error removing bucket integration. {0}'.format(message)

    # Deactivate bucket in db
    if not error:
        # TODO:
        # here we have additional select query because
        # we use procedural helper instead of model helper bucket.deactivate()
        deactivate_bucket(bucket.name)

    return jsonify({
        'error': error,
    })


@s3.route('/api/bucket/<bucket_id>', methods=['DELETE'])
@login_required
def api_bucket_remove(bucket_id):
    error = None

    # Get bucket
    try:
        bucket = (database['session'].query(S3Bucket).
                  filter(S3Bucket.users.any(id=current_user.id)).
                  filter(S3Bucket.id == bucket_id).
                  one())
    except Exception as exception:
        log.exception(exception)
        abort(403)

    # Disable bucket on aws
    if not error:
        success, message = disable_bucket_on_aws(
            bucket.access_key_id,
            bucket.secret_access_key,
            bucket.name)
        if not success:
            error = 'Error removing bucket integration. {0}'.format(message)

    # Delete bucket in db
    if not error:
        database['session'].delete(bucket)
        database['session'].commit()

    return jsonify({
        'error': error,
    })


# Internal

def _check_number_of_buckets(user):

    if (user.plan and user.plan.name != 'free') or user.admin:
        return True

    # Free plan users
    return (get_user_buckets_count(current_user.id) <
            settings.MAX_S3_BUCKETS_ON_FREE_PLAN)


def _run_validation(bucket, job_id):
    # Run validation
    tasks_chain = chain(
        get_validation_conf.s(bucket, job_id=job_id),
        validate.s(job_id=job_id))
    tasks_chain.delay()
