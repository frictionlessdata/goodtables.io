from celery import signals
from goodtablesio import models
from goodtablesio.tasks import validate
from goodtablesio.integrations.github.utils.status import set_commit_status


# Module API

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
    integration_conf = job['integration_conf']

    if integration_conf:

        if task_state == 'SUCCESS' and status != 'running':
            github_status = status
        else:
            github_status = 'error'

        set_commit_status(
           github_status,
           owner=integration_conf['repository']['owner'],
           repo=integration_conf['repository']['name'],
           sha=integration_conf['sha'],
           job_id=job['id'])
