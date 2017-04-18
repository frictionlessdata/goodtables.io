import os

from flask import (
    Blueprint, abort, session, redirect, url_for, send_from_directory, request)
from flask_login import current_user
from sqlalchemy.sql.expression import true

from goodtablesio import models
from goodtablesio.services import database
from goodtablesio.models.source import Source
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

    # Get user sources
    sources = (database['session'].query(Source).
               filter(Source.users.any(id=current_user.id)).
               filter(Source.active == true()).all())

    def sort_sources(source):
        return (source['last_job']['created'].isoformat()
                if source['last_job'] else 'z')

    if sources:
        sources = [source.to_api(with_last_job=True) for source in sources]
        sources = sorted(sources, key=sort_sources)

    return render_component('Dashboard', props={
        'sources': sources,
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
