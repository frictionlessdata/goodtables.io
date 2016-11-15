import uuid
import logging

from flask import Blueprint, request, abort

from goodtablesio.tasks import validate
from goodtablesio.handlers import insert_task_row

from .tasks import clone_repo_files


log = logging.getLogger(__name__)


github = Blueprint('github', __name__, url_prefix='/github')


@github.route('/hook', methods=['POST'])
def create_task():

    # TODO: check origin with secret

    payload = request.get_json()
    if not payload:
        abort(400)

    task_id = str(uuid.uuid4())

    insert_task_row(task_id)

    clone_repo_files.apply_async(
        (payload['repository']['clone_url'], task_id),
        link=validate.s(task_id=task_id))

    return ''
    '''
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
    '''



