from functools import partial
from github3 import GitHub

from goodtablesio import helpers
from goodtablesio.tasks import app as celery_app, JobTask


# Module API

@celery_app.task(name='goodtablesio.github.get_validation_conf', base=JobTask)
def get_validation_conf(owner, repo, job_id):

    # Update job in database
    from goodtablesio.tasks import tasks_db
    tasks_db['jobs'].update({'job_id': job_id, 'status': 'running'}, ['job_id'])

    # Get validation conf
    job_conf_url, job_file_urls = _get_job_urls(owner, repo)
    validation_conf = helpers.prepare_job(job_conf_url, job_file_urls)

    return validation_conf


# Internal

def _get_job_urls(owner, repo):
    make_url = partial(_make_url, owner=owner, repo=repo)
    repo_api = GitHub().repository(owner, repo)
    contents = repo_api.contents('/')
    conf_url = _get_job_conf_url(contents, make_url)
    file_urls = _get_job_file_urls(contents, repo_api, make_url)
    return (conf_url, file_urls)


def _get_job_conf_url(contents, make_url):
    key = 'goodtables.yml'
    if key not in contents:
        return None
    url = make_url(contents[key].path)
    return url


def _get_job_file_urls(contents, repo_api, make_url):
    urls = []
    for key in sorted(contents):
        item = contents[key]
        if item.type == 'file':
            urls.append(make_url(item.path))
        elif item.type == 'dir':
            dir_contents = repo_api.contents(item.path)
            urls.extend(_get_job_file_urls(dir_contents, repo_api, make_url))
    return urls


def _make_url(path, owner, repo, branch='master'):
    template = '{base}/{owner}/{repo}/{branch}/{path}'
    url = template.format(
        base='https://raw.githubusercontent.com',
        owner=owner, repo=repo, branch=branch, path=path)
    return url
