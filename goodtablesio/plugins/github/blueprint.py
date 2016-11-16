import uuid
import logging

from flask import Blueprint, request, abort

from goodtablesio import tasks
from goodtablesio import helpers

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

    helpers.insert_task_row(task_id)

    clone_repo_files.apply_async(
        (payload['repository']['clone_url'], task_id),
        link=tasks.validate.s(task_id=task_id))

    return task_id
