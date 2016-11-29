import uuid
import logging

from flask import Blueprint, request, abort

from goodtablesio import tasks
from goodtablesio import helpers

from goodtablesio.plugins.github.tasks import get_validation_conf


log = logging.getLogger(__name__)


github = Blueprint('github', __name__, url_prefix='/github')


@github.route('/hook', methods=['POST'])
def create_job():

    # TODO: check origin with secret

    payload = request.get_json()
    if not payload:
        abort(400)

    job_id = str(uuid.uuid4())

    helpers.insert_job_row(job_id)

    get_validation_conf.apply_async(
        (payload['repository']['clone_url'], job_id),
        link=tasks.validate.s(job_id))

    return job_id
