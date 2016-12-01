import re
import os
import subprocess
import tempfile
import logging
import shutil

from celery import signals

from goodtablesio import helpers
from goodtablesio.tasks import app as celery_app, validate, JobTask
from goodtablesio.plugins.github.utils import set_commit_status


log = logging.getLogger(__name__)

TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']
CLONE_DIR = '/tmp'


@celery_app.task(name='goodtablesio.github.get_validation_conf', base=JobTask)
def get_validation_conf(clone_url, job_id):
    # We need to import the DB connection at this point, as it has been
    # initialized when the worker started
    from goodtablesio.tasks import tasks_db

    tasks_db['jobs'].update({'job_id': job_id, 'status': 'running'},
                            ['job_id'], ensure=True)

    clone_dir = _clone_repo(job_id, clone_url)
    job_conf_url = _get_job_conf_url(clone_url)
    job_files = _get_job_files(clone_dir)

    # Get job descriptor
    validation_conf = helpers.prepare_job(job_conf_url, job_files)

    # TODO: handle exceptions (eg bad task description)

    _remove_repo(clone_url, clone_dir)

    return validation_conf


@signals.task_postrun.connect(sender=validate)
def post_task_handler(**kwargs):
    # We need to import the DB connection at this point, as it has been
    # initialized when the worker started
    from goodtablesio.tasks import tasks_db

    # We can't use retval because on errors
    # it will be an exception
    job_id = kwargs['kwargs']['job_id']
    job = tasks_db['jobs'].find_one(job_id=job_id)

    if job.get('plugin_name') != 'github':
        return

    task_state = kwargs['state']

    status = job['status']
    plugin_conf = job['plugin_conf']

    if plugin_conf:

        if task_state == 'SUCCESS' and status != 'running':
            github_status = status
        else:
            github_status = 'error'

        set_commit_status(
           github_status,
           owner=plugin_conf['repository']['owner'],
           repo=plugin_conf['repository']['name'],
           sha=plugin_conf['sha'],
           job_id=job['job_id'])


# Internal

def _clone_repo(job_id, clone_url):
    clone_dir = tempfile.mkdtemp(prefix=job_id, dir=CLONE_DIR)

    clone_command = ['git', 'clone', clone_url, clone_dir]
    log.info('Cloning repo {0} into {1}'.format(clone_url, clone_dir))

    try:
        subprocess.check_output(clone_command, stderr=subprocess.STDOUT)

        log.debug('Repo {0} cloned'.format(clone_url))
    except subprocess.CalledProcessError as e:
        log.error(e.output)
        raise e

    return clone_dir


def _get_job_conf_url(clone_url, branch='master'):
    pattern = r'github.com/(?P<user>[^/]*)/(?P<repo>[^/]*)\.git'
    match = re.search(pattern, clone_url)
    user = match.group('user')
    repo = match.group('repo')
    template = '{base}/{user}/{repo}/{branch}/goodtables.yml'
    job_conf = template.format(
        base='https://raw.githubusercontent.com',
        user=user, repo=repo, branch=branch)
    return job_conf


def _get_job_files(top):
    out = []

    for dir_name, sub_dir_list, file_list in os.walk(top, topdown=True):
        if '.git' in sub_dir_list:
            sub_dir_list.remove('.git')
        current_dir = dir_name.replace(top, '').lstrip('/')
        for file_name in file_list:
            if current_dir:
                out.append(os.path.join(current_dir, file_name))
            else:
                out.append(file_name)
    return out


def _remove_repo(clone_url, clone_dir):
    log.debug('Removing repo {0}'.format(clone_url))
    shutil.rmtree(clone_dir)
