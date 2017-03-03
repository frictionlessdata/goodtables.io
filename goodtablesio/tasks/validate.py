import datetime
from copy import deepcopy
from goodtables import Inspector
from goodtablesio import models
from goodtablesio.celery_app import celery_app
from goodtablesio.utils.jobtask import JobTask


# Module API

@celery_app.task(name='goodtablesio.tasks.validate', base=JobTask)
def validate(validation_conf, job_id):
    """Main validation task.

    Args:
        validation_conf (dict): VERIFIED validation conf

    See `schemas/validation-conf.yml`.

    """

    # Get job
    job = models.job.get(job_id)

    # TODO: job not found
    if job['status'] == 'created':
        params = {
            'id': job_id,
            'status': 'running'
        }
        models.job.update(params)

    # Get report
    inspector = Inspector(**validation_conf.get('settings', {}))
    report = inspector.inspect(validation_conf['source'], preset='nested')

    # Save report
    params = {
        'id': job_id,
        'report': report,
        'finished': datetime.datetime.utcnow(),
        'status': 'success' if report['valid'] else 'failure'
    }

    models.job.update(params)

    job.update(params)

    return job
