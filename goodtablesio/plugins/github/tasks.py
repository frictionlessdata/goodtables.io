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
    job_base = _get_job_base(owner, repo)
    job_files = _get_job_files(owner, repo)
    validation_conf = helpers.create_validation_conf(job_base, job_files)

    return validation_conf


# Internal


def _get_job_base(owner, repo, branch='master'):
    template = '{base}/{owner}/{repo}/{branch}'
    baseurl = template.format(
        base='https://raw.githubusercontent.com',
        owner=owner, repo=repo, branch=branch)
    return baseurl


def _get_job_files(owner, repo, repo_api=None, contents=None):
    files = []
    if not repo_api and not contents:
        repo_api = GitHub().repository(owner, repo)
        contents = repo_api.contents('/')
    for key in sorted(contents):
        item = contents[key]
        if item.type == 'file':
            files.append(item.path)
        elif item.type == 'dir':
            dir_contents = repo_api.contents(item.path)
            files.extend(_get_job_files(owner, repo, repo_api, dir_contents))
    return files
