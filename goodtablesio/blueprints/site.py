from flask import Blueprint, abort, render_template, session, redirect, url_for
from flask_login import current_user
from goodtablesio import models


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('site.dashboard'))
    return render_template('index.html', component='Home', props={
        'userName': getattr(current_user, 'display_name', None),
    })


@site.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('site.home'))
    # TODO: Get most recent job per source
    github_jobs = models.job.get_by_integration('github', limit=5)
    s3_jobs = models.job.get_by_integration('s3', limit=5)
    return render_template('index.html', component='Dashboard', props={
        'userName': getattr(current_user, 'display_name', None),
        'githubJobs': github_jobs,
        's3Jobs': s3_jobs,
    })


@site.route('/jobs')
def jobs():
    jobs = models.job.find()
    return render_template('index.html', component='Jobs', props={
        'userName': getattr(current_user, 'display_name', None),
        'jobs': jobs,
    })


@site.route('/jobs/<job_id>')
def job(job_id):
    job = models.job.get(job_id)
    if not job:
        abort(404)
    return render_template('index.html', component='Job', props={
        'userName': getattr(current_user, 'display_name', None),
        'job': job,
    })
