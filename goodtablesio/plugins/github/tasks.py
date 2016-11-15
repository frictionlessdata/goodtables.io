import os
import subprocess
import tempfile
import logging

from goodtablesio.tasks import app as celery_app


log = logging.getLogger(__name__)

TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']
CLONE_DIR = '/tmp'


@celery_app.task(name='goodtablesio.github.clone_repo_files')
def clone_repo_files(clone_url, task_id):

    clone_dir = clone_repo(task_id, clone_url)

    # TODO: take goodtables.yml into account
    paths = get_files_to_validate(clone_dir)

    if paths:
        validation_payload = {
            'source': [{'source': path} for path in paths],
            'preset': 'tables'
        }

        # TODO: set commit status on GitHub

        return validation_payload


def clone_repo(task_id, clone_url):
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


def get_files_to_validate(clone_dir):
    paths = get_dir_paths(clone_dir)
    return get_tabular_file_paths(paths)


def get_dir_paths(top):
    out = []
    for dir_name, sub_dir_list, file_list in os.walk(top, topdown=True):
        if '.git' in sub_dir_list:
            sub_dir_list.remove('.git')
        for file_name in file_list:
            out.append(os.path.join(dir_name, file_name))
    return out


def get_tabular_file_paths(paths):
    out = []
    for path in paths:
        name, extension = os.path.splitext(path)
        if extension and extension[1:].lower() in TABULAR_EXTENSIONS:
            out.append(path)
    return out
