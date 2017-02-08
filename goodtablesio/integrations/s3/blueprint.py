import logging

from flask import (
    Blueprint, render_template, flash, request, redirect,
    url_for, abort, jsonify)
from flask_login import login_required, current_user

from goodtablesio import models
from goodtablesio.services import database
from goodtablesio.integrations.s3.models.bucket import S3Bucket
from goodtablesio.integrations.s3.utils import (
    set_up_bucket_on_aws, create_bucket, get_user_buckets,
    disable_bucket_on_aws, inactivate_bucket)


log = logging.getLogger(__name__)


s3 = Blueprint('s3', __name__, url_prefix='/s3', template_folder='templates')


@s3.record
def record_params(setup_state):
    s3.debug = setup_state.app.debug


@s3.route('/')
def index():

    jobs = models.job.get_by_integration('s3')

    return render_template('s3_home.html', jobs=jobs)


@s3.route('/settings')
@login_required
def settings():

    buckets = get_user_buckets(current_user.id)

    return render_template('s3_settings.html', buckets=buckets)


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
            return redirect(url_for('s3.settings'))

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

    return redirect(url_for('s3.settings'))


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

    return redirect(url_for('s3.settings'))
