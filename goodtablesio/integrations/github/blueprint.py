import logging
from flask import Blueprint, request, abort, jsonify
from flask_login import login_required, current_user
from goodtablesio import settings
from goodtablesio.services import database
from goodtablesio.models.internal_job import InternalJob
from goodtablesio.utils.signature import validate_signature
from goodtablesio.integrations.github.models.repo import GithubRepo
from goodtablesio.integrations.github.tasks.repos import sync_user_repos
from goodtablesio.integrations.github.utils.hook import (
    activate_hook, deactivate_hook, get_details_from_hook_payload)
log = logging.getLogger(__name__)


# Module API

github = Blueprint('github', __name__, url_prefix='/github')


@github.record
def record_params(setup_state):
    github.debug = setup_state.app.debug


@github.route('/hook', methods=['POST'])
def create_job():

    # Validate signature (throws 400 on invalid)
    if not github.debug:
        key = settings.GITHUB_HOOK_SECRET
        text = request.data
        signature = request.headers.get('X-Hub-Signature', '')
        if not validate_signature(key, text, signature):
            msg = 'Wrong signature for GitHub payload'
            log.error(msg)
            abort(400, msg)

    # Get payload details (throws 400 if no data or bad JSON)
    payload = request.get_json()
    details = get_details_from_hook_payload(payload)
    if details is None:
        msg = 'Wrong payload received'
        log.error(msg)
        abort(400, msg)
    if details == {}:
        return jsonify({})

    # Get source (throw 400 if no source)
    source_owner = details['owner']
    source_repo = details['repo']
    if details['is_pr']:
        source_owner = details['base_owner']
        source_repo = details['base_repo']
    source = database['session'].query(GithubRepo).filter(
        GithubRepo.name == '%s/%s' % (source_owner, source_repo)).one_or_none()
    if not source:
        msg = 'A job was requested on a repository not present in the DB'
        log.error(msg)
        abort(400, msg)

    # Create and start job (throw 400 if not started)
    job_id = source.create_and_start_job(conf=details)
    if not job_id:
        msg = 'A job was requested but can\'t be started'
        log.error(msg)
        abort(400, msg)

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

    # Validate repo
    if not error:
        repo.create_and_start_job()

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
