import datetime
from goodtables import Inspector
from goodtablesio import models
from goodtablesio.celery_app import celery_app
from goodtablesio.utils.jobtask import JobTask


# Module API

@celery_app.task(name='goodtablesio.tasks.validate', base=JobTask)
def validate(validation_conf, job_id):
    """Main validation task.

    Args:
        validation_conf (dict): validation configuration

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

    # Safety checks
    if not validation_conf.get('files'):
        params = {
            'id': job_id,
            'finished': datetime.datetime.utcnow(),
            'status': 'error',
            'error': {'message': 'No files to validate'}
        }

    else:
        # Get report
        settings = validation_conf.get('settings', {})
        inspector = Inspector(**settings)
        report = inspector.inspect(validation_conf['files'], preset='tables')

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
