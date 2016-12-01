import datetime
import logging

import dataset
from celery import Celery, signals
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from goodtables import Inspector

from . import config


log = logging.getLogger(__name__)


# Module API

app = Celery('tasks')
app.config_from_object(config)

# TODO: automate
app.autodiscover_tasks(['goodtablesio.plugins.github'])


tasks_db = None


@signals.worker_process_init.connect
def init_worker(**kwargs):
    global tasks_db
    log.debug('Initializing database connection for the worker')
    tasks_db = dataset.connect(
        config.DATABASE_URL,
        engine_kwargs={'pool_size': 20, 'pool_recycle': 3600})


@signals.worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global tasks_db
    if tasks_db:
        log.debug('Closing database connectionn for the worker')
        tasks_db.engine.dispose()


@app.task(name='goodtablesio.tasks.validate')
def validate(validation_conf, job_id):
    """Main validation task.

    Args:
        validation_conf (dict): validation configuration

    See `schemas/validation-conf.yml`.

    """

    job = tasks_db['jobs'].find_one(job_id=job_id)
    # TODO: job not found
    if job['status'] == 'created':
        tasks_db['jobs'].update({'job_id': job_id, 'status': 'running'},
                                ['job_id'])

    # Get report
    settings = validation_conf.get('settings', {})
    inspector = Inspector(**settings)
    report = inspector.inspect(validation_conf['files'], preset='tables')

    # Save report
    job.update({
        'report': report,
        'finished': datetime.datetime.utcnow(),
        'status': 'success' if report['valid'] else 'failure'
    })
    tasks_db['jobs'].update(job,
                            ['job_id'],
                            types={'report': JSONB, 'finished': DateTime},
                            ensure=True)
    return job
