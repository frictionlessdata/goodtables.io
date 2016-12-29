import uuid
import logging

from celery import chain
from flask import Blueprint, request, abort, session
from flask import render_template, jsonify, redirect, url_for
from flask_login import login_required

from goodtablesio import models, settings
from goodtablesio.services import database
from goodtablesio.tasks.validate import validate
from goodtablesio.plugins.github.models.repo import GithubRepo
from goodtablesio.plugins.github.tasks.jobconf import get_validation_conf
from goodtablesio.plugins.github.tasks.repos import sync_user_repositories
from goodtablesio.plugins.github.utils.status import set_commit_status
from goodtablesio.plugins.github.utils.signature import validate_signature
from goodtablesio.plugins.github.utils.hook import get_owner_repo_sha_from_hook_payload


log = logging.getLogger(__name__)


github = Blueprint('github', __name__, url_prefix='/github', template_folder='templates')


@github.route('/hook', methods=['POST'])
def create_job():

    # Validate signature
    key = settings.GITHUB_HOOK_SECRET
    text = request.data
    signature = request.headers.get('X-Hub-Signature', '')
    if not validate_signature(key, text, signature):
        abort(400)

    # Get payload parameters
    payload = request.get_json()
    if not payload:
        abort(400)
    owner, repo, sha = get_owner_repo_sha_from_hook_payload(payload)
    if not owner:
        abort(400)

    # Save job to database
    job_id = str(uuid.uuid4())
    plugin_conf = {
        'repository': {
            'owner': owner,
            'name': repo,
            },
        'sha': sha,
    }
    models.job.create({
        'id': job_id,
        'plugin_name': 'github',
        'plugin_conf': plugin_conf,
    })

    # Set GitHub status
    set_commit_status(
        'pending',
        owner=owner,
        repo=repo,
        sha=sha,
        job_id=job_id)

    # Run validation
    tasks_chain = chain(
        get_validation_conf.s(owner, repo, sha, job_id=job_id),
        validate.s(job_id=job_id))
    tasks_chain.delay()

    return jsonify({'job_id': job_id})


@github.route('/repos')
@login_required
def repos():

    # Get github syncing status
    github_sync = False
    if session.get('github_sync_task_id'):
        task_id = session['github_sync_task_id']
        result = sync_user_repositories.AsyncResult(task_id)
        if result.status == 'PENDING':
            github_sync = True
        else:
            # TODO: cover errors
            del session['github_sync_task_id']

    # Get github repos
    github_repos = []
    if not github_sync:
        user_id = session['user_id']
        github_repos = (database['session'].query(GithubRepo).
            filter(GithubRepo.users.any(id=user_id)).
            order_by(GithubRepo.owner, GithubRepo.repo).
            all())

    return render_template('repos.html',
        github_sync=github_sync,
        github_repos=github_repos)


@github.route('/sync')
@login_required
def sync_account():
    # TODO: cover case when session doens't have github_token
    user_id = session['user_id']
    github_token = session['auth_github_token'][0]
    result = sync_user_repositories.delay(user_id, github_token)
    # TODO: store in the database (not session)
    # It's kinda general problem it looks like we need
    # to track syncing tasks in the database (github, s3, etc)
    session['github_sync_task_id'] = result.task_id
    return redirect(url_for('github.repos'))
