import logging
import datetime

from github3 import GitHub

from goodtablesio import models, settings
from goodtablesio.services import database
from goodtablesio.models.user import User
from goodtablesio.models.github_repo import GithubRepo
from goodtablesio.tasks import app as celery_app, JobTask
from goodtablesio.utils.jobconf import create_validation_conf
from goodtablesio.plugins.github.utils import iter_repos_by_token

# Register signals
import goodtablesio.plugins.github.signals  # noqa

log = logging.getLogger(__name__)
session = database['session']


# Module API

@celery_app.task(name='goodtablesio.github.get_validation_conf', base=JobTask)
def get_validation_conf(owner, repo, sha, job_id):
    """Celery tast to get validation conf.
    """

    # Update job
    models.job.update({
        'id': job_id,
        'status': 'running'
    })

    # Get validation conf
    job_base = _get_job_base(owner, repo, sha)
    job_files = _get_job_files(owner, repo, sha)
    validation_conf = create_validation_conf(job_base, job_files)

    return validation_conf


@celery_app.task(name='goodtablesio.github.collect_user_repositories')
def sync_user_repositories(user_id, token):
    """Sync user repositories.
    """
    # TODO: rewrite using sqlalchemy query
    session.execute(
        'DELETE FROM users_github_repos WHERE user_id = :user_id',
        {'user_id': user_id})
    user = session.query(User).get(user_id)
    for repo_data in iter_repos_by_token(token):
        repo = session.query(GithubRepo).get(repo_data['id'])
        if repo is None:
            repo = GithubRepo(**repo_data)
            session.add(repo)
        repo.active = repo_data['active']
        repo.updated = datetime.datetime.utcnow(),
        repo.users.append(user)
        # TODO: remove
        if repo_data['repo'] == 'example-goodtables.io':
            break
    session.commit()


# Internal


def _get_job_base(owner, repo, sha):
    """Get job's base url.
    """
    template = '{base}/{owner}/{repo}/{sha}'
    baseurl = template.format(
        base='https://raw.githubusercontent.com',
        owner=owner, repo=repo, sha=sha)
    return baseurl


def _get_job_files(owner, repo, sha):
    """Get job's files.
    """
    github_api = GitHub(token=settings.GITHUB_API_TOKEN)
    repo_api = github_api.repository(owner, repo)
    # First attempt - use GitHub Tree API
    files = _get_job_files_tree_api(repo_api, sha)
    if files is None:
        # Tree is trancated - use GitHub Contents API
        files = _get_job_files_contents_api(repo_api, sha)
    log.debug(
        'Remaining GitHub API calls: %s',
        github_api.rate_limit()['rate']['remaining'])
    return files


def _get_job_files_tree_api(repo_api, sha):
    """Get job's files using GitHub Tree API.
    """
    files = []
    # https://github.com/sigmavirus24/github3.py/issues/656
    tree = repo_api.tree('%s?recursive=1' % sha).to_json()
    if tree['truncated']:
        return None
    for item in tree['tree']:
        if item['type'] == 'blob':
            files.append(item['path'])
    return files


def _get_job_files_contents_api(repo_api, sha, contents=None):
    """Get job's files using GitHub Contents API.
    """
    files = []
    if not contents:
        contents = repo_api.contents('', sha)
    for key in sorted(contents):
        item = contents[key]
        if item.type == 'file':
            files.append(item.path)
        elif item.type == 'dir':
            dir_contents = repo_api.contents(item.path, sha)
            files.extend(_get_job_files_contents_api(repo_api, sha, dir_contents))
    return files
