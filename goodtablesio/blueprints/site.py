from flask import Blueprint, abort, render_template
from goodtablesio import helpers


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    return 'goodtables.io'


@site.route('/job/<job_id>')
def job(job_id):
    job = helpers.get_job(job_id)
    if not job:
        abort(404)
    return render_template('job.html', job=job)
