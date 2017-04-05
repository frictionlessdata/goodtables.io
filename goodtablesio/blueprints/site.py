import os

from flask import (
    Blueprint, abort, session, redirect, url_for, send_from_directory, request)

from goodtablesio import models
from goodtablesio.services import database
from goodtablesio.utils.frontend import render_component


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    if session.get('user_id'):
        return redirect(url_for('site.dashboard'))
    return render_component('Home')


@site.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('site.home'))

    # TODO: Get most recent job per source

    github_jobs = models.job.get_by_integration('github', limit=5)
    s3_jobs = models.job.get_by_integration('s3', limit=5)

    latest_jobs = github_jobs + s3_jobs

    return render_component('Dashboard', props={
        'latestJobs': latest_jobs,
    })


@site.route('/jobs')
def jobs():
    jobs = models.job.find()
    return render_component('Jobs', props={
        'jobs': jobs,
    })


@site.route('/jobs/<job_id>')
def job(job_id):
    job = models.job.get(job_id)
    if not job:
        abort(404)
    return render_component('Job', props={
        'job': job,
    })


@site.route('/badge/<integration_name>/<path:source_name>.svg')
def badge(integration_name, source_name):

    last_status = (
        database['session'].query(models.job.Job.status).
        join(models.source.Source).
        filter(models.job.Job.integration_name == integration_name).
        filter(models.job.Job.status.in_(['success', 'failure', 'error'])).
        filter((models.source.Source.name == source_name) |
               (models.source.Source.id == source_name)).
        order_by(models.job.Job.finished.desc()).
        limit(1).
        one_or_none()
    )

    style = request.args.get('style', 'flat')
    if style not in ('flat', 'flat-square'):
        style = 'flat'

    if last_status:
        last_status = last_status[0]
    else:
        last_status = 'unknown'

    file_name = 'data-{status}-{style}.svg'.format(
        status=last_status, style=style)

    file_path = os.path.join(
        os.path.dirname(__file__), 'badges')

    return send_from_directory(file_path, file_name, mimetype='image/svg+xml')
