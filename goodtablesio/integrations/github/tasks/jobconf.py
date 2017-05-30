import logging
import requests
from github3 import GitHub
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.celery_app import celery_app
from goodtablesio.tasks.base import JobTask
from goodtablesio.utils.jobconf import make_validation_conf
log = logging.getLogger(__name__)


# Module API

@celery_app.task(name='goodtablesio.github.get_validation_conf', base=JobTask)
def get_validation_conf(owner, repo, sha, job_id, tokens):
    """Celery tast to get validation conf.
    """

    job = database['session'].query(Job).get(job_id)

    job.status = 'running'
    database['session'].add(job)
    database['session'].commit()

    # Get validation conf
    job_base = _get_job_base(owner, repo, sha)
    job_files = _get_job_files(owner, repo, sha, tokens)
    job_conf_text = _load_job_conf_text(job_base)
    validation_conf = make_validation_conf(job_conf_text, job_files, job_base)

    return validation_conf


# Internal

def _get_job_base(owner, repo, sha):
    """Get job's base url.
    """
    template = '{base}/{owner}/{repo}/{sha}'
    baseurl = template.format(
        base='https://raw.githubusercontent.com',
        owner=owner, repo=repo, sha=sha)
    return baseurl


def _get_job_files(owner, repo, sha, tokens):
    """Get job's files.
    """
    # TODO: use other tokens if first fails
    github_api = GitHub(token=tokens[0])
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
            files.extend(
                _get_job_files_contents_api(repo_api, sha, dir_contents))
    return files


def _load_job_conf_text(job_base):
    url = '/'.join([job_base, 'goodtables.yml'])
    text = _load_file(url)
    return text


def _load_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
