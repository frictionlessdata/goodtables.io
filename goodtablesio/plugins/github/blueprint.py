import uuid
import logging

from celery import chain
from flask import Blueprint, request, abort

from goodtablesio import tasks
from goodtablesio import helpers

from goodtablesio.plugins.github.tasks import get_validation_conf
from goodtablesio.plugins.github.utils import set_commit_status


log = logging.getLogger(__name__)


github = Blueprint('github', __name__, url_prefix='/github')


@github.route('/hook', methods=['POST'])
def create_job():

    # TODO: check origin with secret

    payload = request.get_json()
    if not payload:
        abort(400)

    job_id = str(uuid.uuid4())

    # Store these details to be used when the job finishes
    plugin_conf = {
        'repository': {
            'owner': payload['repository']['owner']['name'],
            'name': payload['repository']['name'],
            },
        'sha': payload['head_commit']['id'],
    }

    helpers.insert_job_row(job_id, 'github', plugin_conf=plugin_conf)

    set_commit_status(
        'pending',
        owner=payload['repository']['owner']['name'],
        repo=payload['repository']['name'],
        sha=payload['head_commit']['id'],
        job_id=job_id)

    tasks_chain = chain(
        get_validation_conf.s(payload['repository']['clone_url'], job_id=job_id),
        tasks.validate.s(job_id=job_id))
    tasks_chain.delay()

    return job_id
