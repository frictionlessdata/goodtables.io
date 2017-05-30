from celery import signals
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.tasks.validate import validate
from goodtablesio.integrations.github.utils.status import set_commit_status


# Module API

@signals.task_postrun.connect(sender=validate)
def post_task_handler(**kwargs):

    job_id = kwargs['kwargs']['job_id']
    job = database['session'].query(Job).get(job_id)

    if job.integration_name != 'github':
        return

    task_state = kwargs['state']

    if job.conf:

        if task_state == 'SUCCESS' and job.status != 'running':
            github_status = job.status
        else:
            github_status = 'error'

        set_commit_status(
           github_status,
           owner=job.conf['owner'],
           repo=job.conf['repo'],
           sha=job.conf['sha'],
           job_number=job.number,
           is_pr=job.conf['is_pr'],
           tokens=job.source.tokens)
