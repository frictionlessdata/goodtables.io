from flask import Blueprint, abort, render_template, session, redirect, url_for
from goodtablesio import models


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('site.dashboard'))
    return render_template('index.html', route='Home')


@site.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('site.home'))
    # TODO: Get most recent job per source
    github_jobs = models.job.get_by_integration('github', limit=5)
    s3_jobs = models.job.get_by_integration('s3', limit=5)
    return render_template('index.html', route='Dashboard', props={
      'githubJobs': github_jobs,
      's3Jobs': s3_jobs,
    })


@site.route('/jobs')
def jobs():
    jobs = models.job.find()
    return render_template('index.html', route='Jobs', props={
      'jobs': jobs,
    })


@site.route('/jobs/<job_id>')
def job(job_id):
    job = models.job.get(job_id)
    if not job:
        abort(404)
    return render_template('index.html', route='Job', props={
      'job': job,
    })
