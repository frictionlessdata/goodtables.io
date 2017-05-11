import datetime
from goodtables import Inspector
from goodtablesio import models, settings
from goodtablesio.celery_app import celery_app
from goodtablesio.tasks.base import JobTask


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
    if 'settings' not in validation_conf:
        validation_conf['settings'] = {}

    max_tables = settings.MAX_TABLES_PER_SOURCE
    if (not validation_conf['settings'].get('table_limit') or
            validation_conf['settings']['table_limit'] > max_tables):
        validation_conf['settings']['table_limit'] = max_tables
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
