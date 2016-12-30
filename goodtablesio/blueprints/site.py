from flask import Blueprint, abort, render_template, session
from goodtablesio.services import database
from goodtablesio import models


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    user_jobs = []
    user_id = session.get('user_id')
    if user_id:
        # TODO: here we should filter jobs by user!
        user_jobs = database['session'].query(models.job.Job).all()
    return render_template('home.html', user_jobs=user_jobs)


@site.route('/jobs')
def jobs():
    job_ids = models.job.get_ids()
    return render_template('jobs.html', job_ids=job_ids)


@site.route('/jobs/<job_id>')
def job(job_id):
    job = models.job.get(job_id)
    if not job:
        abort(404)
    return render_template('job.html', job=job)


@site.route('/integrations')
def integrations():
    return render_template('integrations.html')
