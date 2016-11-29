import re
import os
import subprocess
import tempfile
import logging
import shutil

from goodtablesio import helpers
from goodtablesio.tasks import app as celery_app


log = logging.getLogger(__name__)

TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']
CLONE_DIR = '/tmp'


@celery_app.task(name='goodtablesio.github.get_validation_conf')
def get_validation_conf(clone_url, job_id):

    clone_dir = _clone_repo(job_id, clone_url)
    job_conf = _get_job_conf(clone_url)
    job_files = _get_job_files(clone_dir)

    # Get job descriptor
    validation_conf = helpers.prepare_job(job_conf, job_files)

    # TODO: handle exceptions (eg bad task description)

    _remove_repo(clone_url, clone_dir)

    return validation_conf


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


def _get_job_conf(clone_url, branch='master'):
    pattern = r'github.com/(?P<user>[^/]*)/(?P<repo>[^/]*)\.git'
    match = re.search(pattern, clone_url)
    user = match.group('user')
    repo = match.group('repo')
    template = 'https://raw.githubusercontent.com/{user}/{repo}/{branch}/goodtables.yml'
    job_conf = template.format(user=user, repo=repo, branch=branch)
    return job_conf


def _get_job_files(top):
    out = []
    for dir_name, sub_dir_list, file_list in os.walk(top, topdown=True):
        if '.git' in sub_dir_list:
            sub_dir_list.remove('.git')
        for file_name in file_list:
            out.append(file_name)
    return out


def _remove_repo(clone_url, clone_dir):
    log.info('Removing repo {0} from {1}'.format(clone_url, clone_dir))
    shutil.rmtree(clone_dir)
