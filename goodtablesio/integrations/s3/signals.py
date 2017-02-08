from urllib.parse import urlparse

from celery import signals
import urllib

from goodtablesio import models
from goodtablesio.tasks.validate import validate


@signals.task_postrun.connect(sender=validate)
def post_task_handler(**kwargs):

    job = kwargs['retval']
    if isinstance(kwargs['retval'], Exception):
        job_id = kwargs['kwargs']['job_id']
        job = models.job.get(job_id)

    if job.get('integration_name') != 's3':
        return

    if job.get('report') and job['report'].get('tables'):
        tables = job['report']['tables']
        for table in tables:
            parts = urlparse(table['source'])
            table['source'] = urllib.parse.unquote(parts.path.lstrip('/'))
        models.job.update({'id': job['id'], 'report': job['report']})
