import os
import re
import datetime
from goodtables import Inspector
from goodtablesio import models, settings
from goodtablesio.celery_app import celery_app
from goodtablesio.tasks.base import JobTask


# Module API

@celery_app.task(name='goodtablesio.tasks.validate', base=JobTask)
def validate(validation_conf, job_id, files={}):
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

    # Add uploaded files
    for item in validation_conf['source']:
        if item.get('preset', 'table') in ['table', 'datapackage']:
            item['scheme'] = 'http'
            if item['source'] in files:
                item['scheme'] = 'file'
                item['source'] = files[item['source']]
            if item.get('schema') in files:
                item['schema'] = files[item['schema']]

    # Get report
    if 'settings' not in validation_conf:
        validation_conf['settings'] = {}
    max_tables = settings.MAX_TABLES_PER_SOURCE
    if (not validation_conf['settings'].get('table_limit') or
            validation_conf['settings']['table_limit'] > max_tables):
        validation_conf['settings']['table_limit'] = max_tables
    inspector = Inspector(**validation_conf.get('settings', {}))
    report = inspector.inspect(validation_conf['source'], preset='nested')

    # Hide uploaded files
    for table in report['tables']:
        if table['source'].startswith('/'):
            table['source'] = os.path.basename(table['source'])
    for index, warning in enumerate(report['warnings']):
        report['warnings'][index] = re.sub(r'/tmp/.*?/', '', warning)

    # Save report
    params = {
        'id': job_id,
        'finished': datetime.datetime.utcnow(),
    }
    if report['table-count'] > 0:
        params.update({
            'status': 'success' if report['valid'] else 'failure',
            'report': report,
        })
    else:
        params.update({
            'status': 'error',
            'error': {'message': '\n'.join(report['warnings']) or 'No tables found'},
        })
    models.job.update(params)
    job.update(params)

    return job
