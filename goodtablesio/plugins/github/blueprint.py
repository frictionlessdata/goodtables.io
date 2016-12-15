import uuid
import logging

from celery import chain
from flask import Blueprint, request, abort

from goodtablesio import tasks, models

from goodtablesio.plugins.github.tasks import get_validation_conf
from goodtablesio.plugins.github.utils import set_commit_status


log = logging.getLogger(__name__)


github = Blueprint('github', __name__, url_prefix='/github')


@github.route('/hook', methods=['POST'])
def create_job():

    # Get parameters from payload
    payload = request.get_json()
    if not payload:
        abort(400)
    owner = payload['repository']['owner']['name']
    repo = payload['repository']['name']
    sha = payload['head_commit']['id']

    # Save job to database
    job_id = str(uuid.uuid4())
    plugin_conf = {
        'repository': {
            'owner': owner,
            'name': repo,
            },
        'sha': sha,
    }

    models.job.create({
        'id': job_id,
        'plugin_name': 'github',
        'plugin_conf': plugin_conf
    })

    # Set GitHub status
    set_commit_status(
        'pending',
        owner=owner,
        repo=repo,
        sha=sha,
        job_id=job_id)

    # Run validation
    tasks_chain = chain(
        get_validation_conf.s(owner, repo, sha, job_id=job_id),
        tasks.validate.s(job_id=job_id))
    tasks_chain.delay()

    return job_id
