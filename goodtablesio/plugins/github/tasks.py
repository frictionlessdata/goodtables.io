import re
import os
import subprocess
import tempfile
import logging

from goodtablesio import helpers
from goodtablesio.tasks import app as celery_app


log = logging.getLogger(__name__)

TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']
CLONE_DIR = '/tmp'


@celery_app.task(name='goodtablesio.github.get_task_desc')
def get_task_desc(clone_url, task_id):

    clone_dir = _clone_repo(task_id, clone_url)
    task_conf = _get_task_conf(clone_url)
    task_files = _get_task_files(clone_dir)

    # Get task descriptor
    task_desc = helpers.prepare_task(task_conf, task_files)

    # TODO: handle exceptions (eg bad task description)
    # TODO: cleanup clone dirs

    return task_desc


# Internal

def _clone_repo(task_id, clone_url):
    clone_dir = tempfile.mkdtemp(prefix=task_id, dir=CLONE_DIR)

    clone_command = ['git', 'clone', clone_url, clone_dir]
    log.info('Cloning repo {0} into {1}'.format(clone_url, clone_dir))

    try:
        subprocess.check_output(clone_command, stderr=subprocess.STDOUT)

        log.debug('Repo {0} cloned'.format(clone_url))
    except subprocess.CalledProcessError as e:
        log.error(e.output)
        raise e

    return clone_dir


def _get_task_conf(clone_url, branch='master'):
    pattern = r'github.com/(?P<user>[^/]*)/(?P<repo>[^/]*)\.git'
    match = re.search(pattern, clone_url)
    user = match.group('user')
    repo = match.group('repo')
    template = 'https://raw.githubusercontent.com/{user}/{repo}/{branch}/goodtables.yml'
    task_conf = template.format(user=user, repo=repo, branch=branch)
    return task_conf


def _get_task_files(top):
    out = []
    for dir_name, sub_dir_list, file_list in os.walk(top, topdown=True):
        if '.git' in sub_dir_list:
            sub_dir_list.remove('.git')
        for file_name in file_list:
            out.append(file_name)
    return out
