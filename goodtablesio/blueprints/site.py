from flask import Blueprint, abort, render_template
from goodtablesio import helpers


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    return render_template('home.html')


@site.route('/job')
def jobs():
    job_ids = helpers.get_job_ids()
    return render_template('jobs.html', job_ids=job_ids)


@site.route('/job/<job_id>')
def job(job_id):
    job = helpers.get_job(job_id)
    if not job:
        abort(404)
    return render_template('job.html', job=job)
