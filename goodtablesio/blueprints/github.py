import re
import os
import subprocess
import tempfile
import uuid
import logging
from flask import Blueprint, request, abort
from .. import exceptions
from .. import helpers
log = logging.getLogger(__name__)


SECRET = 'HUGI#6A2X|e{.Rkn`zg?a!`/9(&(Y7WYQqW#5.(&][s&-W(A8y;85pC:&;H<v*aw'
CLONE_DIR = '/tmp'


github = Blueprint('github', __name__, url_prefix='/github')


@github.route('/hook', methods=['POST'])
def create_task():

    # TODO: check origin with secret
    # TODO: process errors

    # Get payload
    payload = request.get_json()
    if not payload:
        abort(400)

    # Get task id
    task_id = str(uuid.uuid4())

    # Get task configuration and files
    clone_url = payload['repository']['clone_url']
    clone_dir = _clone_repo(task_id, clone_url)
    task_conf = _get_task_conf(clone_url)
    task_files = _get_task_files(clone_dir)

    # Get task descriptor
    try:
        task_desc = helpers.prepare_task(task_conf, task_files)
    except exceptions.InvalidTaskConfiguration:
        abort(400)

    # Create task
    try:
        helpers.create_task(task_desc, task_id=task_id)
    except exceptions.InvalidTaskDescriptor:
        abort(400)

    # TODO: cleanup clone dirs

    return task_id


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
