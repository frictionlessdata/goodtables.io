import os
from flask import Blueprint, abort, redirect, url_for, send_from_directory, request
from flask_login import current_user
from sqlalchemy.sql.expression import true
from goodtablesio import models
from goodtablesio import settings
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.models.source import Source
from goodtablesio.utils.frontend import render_component
from goodtablesio.utils.backend import no_cache


# Module API

site = Blueprint('site', __name__)


@site.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('site.dashboard'))
    return render_component('Home')


@site.route('/demo')
def demo():
    return render_component('DemoForm', props={
        'apiUrl': settings.DEMO_API_URL,
        'apiToken': settings.DEMO_API_TOKEN,
        'apiSourceId': settings.DEMO_API_SOURCE_ID,
    })


@site.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))

    # Get user sources
    sources = (database['session'].query(Source).join(Job, isouter=True).
               filter(Source.users.any(id=current_user.id)).
               filter(Source.active == true()).
               order_by(Job.created.desc().nullslast(), Source.name).all())

    if sources:
        sources = [source.to_api(with_last_job=True) for source in sources]

    return render_component('Dashboard', props={
        'sources': sources,
    })


@site.route('/github/<owner>/<repo>')
def source_github(owner, repo):
    return _source('github', '/'.join([owner, repo]))


@site.route('/github/<owner>/<repo>/jobs/<int:job>')
def source_github_job(owner, repo, job):
    return _source('github', '/'.join([owner, repo]), job)


@site.route('/s3/<bucket>')
def source_s3(bucket):
    return _source('s3', bucket)


@site.route('/s3/<bucket>/jobs/<int:job>')
def source_s3_job(bucket, job):
    return _source('s3', bucket, job)


@site.route('/settings')
def settings_page():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))
    return render_component('Settings')


@site.route('/badge/<integration_name>/<path:source_name>.svg')
@no_cache
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


# Internal

def _source(integration_name, name, job_number=None):

    # Get source
    source = (database['session'].query(Source).
              filter(Source.integration_name == integration_name).
              filter(Source.name == name).
              first())
    if not source:
        abort(404)

    # Check access
    if not _check_source_access(source):
        abort(401, 'You are not authorized to access this source')

    # Get selected job
    if job_number:
        job = (database['session'].query(Job).
               filter(Job.source == source).
               filter(Job.number == job_number).
               first())
        if not job:
            abort(404)

    # Get default job
    else:
        job = source.last_job

    return render_component('Source', props={
        'source': source.to_api(with_job_history=True),
        'job': job.to_api() if job else None,
    })


def _check_source_access(source):

    anon = not current_user.is_authenticated

    # Public GitHub repos can be accessed by anybody
    if (source.integration_name == 'github' and
            not source.conf.get('private', True)):
        return True

    # For all the other sources, user must be at least logged in
    if anon:
        return False

    # Admins can see everything
    if current_user.admin:
        return True

    # Simple check for now. You can only see your own S3 buckets or private
    # repos linked to your account (eventually this will mean that there is
    # a paid subcription linked to the GitHub org)
    return current_user.id in [u.id for u in source.users]
