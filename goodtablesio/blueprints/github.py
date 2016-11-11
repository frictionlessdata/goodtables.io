import os
import subprocess
import tempfile
import uuid
import logging

from flask import Blueprint, request, abort

from goodtablesio import handlers


log = logging.getLogger(__name__)


TABULAR_EXTENSIONS = ['csv', 'xls', 'xlsx', 'ods']
CLONE_DIR = '/tmp'


github = Blueprint('github', __name__, url_prefix='/github')

SECRET = 'HUGI#6A2X|e{.Rkn`zg?a!`/9(&(Y7WYQqW#5.(&][s&-W(A8y;85pC:&;H<v*aw'


@github.route('/hook', methods=['POST'])
def create_task():

    # TODO: check origin with secret

    payload = request.get_json()
    if not payload:
        abort(400)

    task_id = str(uuid.uuid4())

    clone_dir = clone_repo(task_id, payload['repository']['clone_url'])

    # TODO: take goodtables.yml into account
    paths = get_files_to_validate(clone_dir)

    if paths:
        validation_payload = {
            'source': [{'source': path} for path in paths],
            'preset': 'tables'
        }
        handlers.create_task(validation_payload, task_id=task_id)

        # TODO: set commit status on GitHub

        return task_id

    return ''

    # TODO: cleanup clone dirs


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
