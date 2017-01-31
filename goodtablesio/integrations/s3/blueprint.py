import logging

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required

from goodtablesio import models

from goodtablesio.integrations.s3.utils import set_up_bucket


log = logging.getLogger(__name__)


s3 = Blueprint('s3', __name__, url_prefix='/s3', template_folder='templates')


@s3.route('/')
def index():

    jobs = models.job.get_by_integration('s3')

    return render_template('s3_home.html', jobs=jobs)


@s3.route('/settings')
@login_required
def settings():

    return render_template('s3_settings.html')


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
        success, message = set_up_bucket(
            access_key_id, secret_access_key, bucket_name)

        # Redirect and flash message
        if success:
            flash('Bucket added', 'success')
        else:
            flash('Error setting up bucket integration. {0}'.format(message),
                  'danger')

    return redirect(url_for('s3.settings'))
