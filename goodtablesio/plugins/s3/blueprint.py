import logging

from flask import Blueprint, render_template
from flask_login import login_required

from goodtablesio import models


log = logging.getLogger(__name__)


s3 = Blueprint('s3', __name__, url_prefix='/s3', template_folder='templates')


@s3.route('/')
def index():

    jobs = models.job.get_by_plugin('s3')

    return render_template('s3_home.html', jobs=jobs)


@s3.route('/settings')
@login_required
def s3_settings():

    return render_template('s3_settings.html')
