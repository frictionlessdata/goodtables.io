import uuid
import logging

from celery import chain
from flask import Blueprint, request, abort, jsonify
from flask_login import login_required, current_user

from goodtablesio import models, settings
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.models.internal_job import InternalJob
from goodtablesio.tasks.validate import validate
from goodtablesio.utils.signature import validate_signature
from goodtablesio.utils.frontend import render_component
from goodtablesio.integrations.github.models.repo import GithubRepo
from goodtablesio.integrations.github.tasks.jobconf import get_validation_conf
from goodtablesio.integrations.github.tasks.repos import sync_user_repos
from goodtablesio.integrations.github.utils.status import set_commit_status
from goodtablesio.integrations.github.utils.hook import (
    activate_hook, deactivate_hook, get_owner_repo_sha_from_hook_payload,
    get_tokens_for_job)


log = logging.getLogger(__name__)


github = Blueprint('github', __name__, url_prefix='/github')


@github.record
def record_params(setup_state):
    github.debug = setup_state.app.debug


@github.route('/settings')
@login_required
def github_settings():
    return render_component('GithubSettings')


@github.route('/hook', methods=['POST'])
def create_job():

    # Validate signature
    if not github.debug:
        key = settings.GITHUB_HOOK_SECRET
        text = request.data
        signature = request.headers.get('X-Hub-Signature', '')
        if not validate_signature(key, text, signature):
            msg = 'Wrong signature for GitHub payload'
            log.error(msg)
            abort(400, msg)

    # Get payload parameters
    payload = request.get_json()
    if not payload:
        msg = 'No payload received'
        log.error(msg)
        abort(400, msg)

    owner, repo, sha = get_owner_repo_sha_from_hook_payload(payload)
    if not owner:
        msg = 'Wrong payload received'
        log.error(msg)
        abort(400, msg)

    # Check repo exists
    source = database['session'].query(GithubRepo).filter(
        GithubRepo.name == '{0}/{1}'.format(owner, repo)).one_or_none()

    if not source:
        msg = 'A job was requested on a repository not present in the DB'
        log.error(msg)
        abort(400, msg)

    # Save job to database
    job_id = str(uuid.uuid4())
    params = {
        'id': job_id,
        'integration_name': 'github',
        'source_id': source.id,
        'conf': {
            'owner': owner,
            'repo': repo,
            'sha': sha,
        }
    }
    job = Job(**params)
    job.source = source

    database['session'].add(job)
    database['session'].commit()

    tokens = get_tokens_for_job(job)

    # Set GitHub status
    set_commit_status(
        'pending',
        owner=owner,
        repo=repo,
        sha=sha,
        job_id=job_id,
        tokens=tokens)

    # Run validation
    tasks_chain = chain(
        get_validation_conf.s(owner, repo, sha, job_id=job_id),
        validate.s(job_id=job_id))
    tasks_chain.delay()

    return jsonify({'job_id': job_id})


# API

# TODO:
# it should be synced with general
# approach we use for API (see api blueprint)

@github.route('/api/sync_account')
@login_required
def api_sync_account():
    error = None

    # Check syncing status
    if _is_user_repos_syncing(current_user.id):
        error = 'User repos are already syncing'

    # Run syncing
    if not error:
        # TODO:
        # Job create/run should be atomic
        # https://github.com/frictionlessdata/goodtables.io/issues/172
        job = InternalJob(name=sync_user_repos.name, user=current_user)
        database['session'].add(job)
        database['session'].commit()
        sync_user_repos.delay(current_user.id, job_id=job.id)

    return jsonify({
        'error': error,
    })


@github.route('/api/repo/<repo_id>')
@login_required
def api_repo(repo_id):
    error = None
    repo_data = None

    # Get repo
    try:
        repo = (database['session'].query(GithubRepo).
                filter(GithubRepo.users.any(id=current_user.id)).
                filter(GithubRepo.id == repo_id).
                one())
        repo_data = repo.to_api()
    except Exception as exception:
        log.exception(exception)
        abort(403)

    return jsonify({
        'repo': repo_data,
        'error': error,
    })


@github.route('/api/repo')
@login_required
def api_repo_list():
    error = None

    # Get repos
    repos = (
        database['session'].query(GithubRepo).
        filter(GithubRepo.users.any(id=current_user.id)).
        order_by(GithubRepo.active.desc(), GithubRepo.name).
        all())
    repos_data = [repo.to_api() for repo in repos]

    # Get syncing status
    syncing = _is_user_repos_syncing(current_user.id)

    return jsonify({
        'repos': repos_data,
        'syncing': syncing,
        'error': error,
    })


@github.route('/api/repo/<repo_id>/activate')
@login_required
def api_repo_activate(repo_id):
    error = None

    # Get token
    token = current_user.github_oauth_token
    if not token:
        error = 'No valid GitHub token found'

    # Get repo
    if not error:
        try:
            repo = (database['session'].query(GithubRepo).
                    filter(GithubRepo.users.any(id=current_user.id)).
                    filter(GithubRepo.id == repo_id).
                    one())
        except Exception as exception:
            log.exception(exception)
            abort(403)

    # Activate repo
    if not error:
        try:
            activate_hook(token, repo.owner, repo.repo)
            repo.active = True
            database['session'].commit()
        except Exception as exception:
            error = 'Repo activation error'
            log.exception(exception)

    return jsonify({
        'error': error,
    })


@github.route('/api/repo/<repo_id>/deactivate')
@login_required
def api_repo_deactivate(repo_id):
    error = None

    # Get token
    token = current_user.github_oauth_token
    if not token:
        error = 'No valid GitHub token found'

    # Get repo
    if not error:
        try:
            repo = (database['session'].query(GithubRepo).
                    filter(GithubRepo.users.any(id=current_user.id)).
                    filter(GithubRepo.id == repo_id).
                    one())
        except Exception as exception:
            log.exception(exception)
            abort(403)

    # Deactivate repo
    if not error:
        try:
            deactivate_hook(token, repo.owner, repo.repo)
            repo.active = False
            database['session'].commit()
        except Exception as exception:
            log.exception(exception)
            error = 'Repo deactivation error'

    return jsonify({
        'error': error,
    })


# Internal

def _is_user_repos_syncing(user_id):
    return bool(
        database['session'].query(InternalJob).
        filter_by(
            name=sync_user_repos.name,
            user_id=user_id,
            finished=None).
        count())
