from celery import signals

from goodtablesio import models
from goodtablesio.tasks.validate import validate
from goodtablesio.integrations.github.utils.status import set_commit_status


@signals.task_postrun.connect(sender=validate)
def post_task_handler(**kwargs):

    job = kwargs['retval']
    if isinstance(kwargs['retval'], Exception):
        job_id = kwargs['kwargs']['job_id']
        job = models.job.get(job_id)

    if job.get('integration_name') != 'github':
        return

    task_state = kwargs['state']

    status = job['status']
    conf = job['conf']

    if conf:

        if task_state == 'SUCCESS' and status != 'running':
            github_status = status
        else:
            github_status = 'error'

        set_commit_status(
           github_status,
           owner=conf['owner'],
           repo=conf['repo'],
           sha=conf['sha'],
           job_id=job['id'])
