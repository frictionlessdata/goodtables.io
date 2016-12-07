import datetime
import logging

from celery import Celery, Task, signals
from goodtables import Inspector

from . import config
from . import exceptions
from . import helpers
from .services import get_engine, make_db_session


log = logging.getLogger(__name__)


# Module API

app = Celery('tasks')
app.config_from_object(config)

# TODO: automate
app.autodiscover_tasks(['goodtablesio.plugins.github'])


tasks_db_engine = None
tasks_db_session = None


@signals.worker_process_init.connect
def init_worker(**kwargs):
    global tasks_db_engine, tasks_db_session
    log.debug('Initializing database connection for the worker')
    tasks_db_engine = get_engine()
    tasks_db_session = make_db_session(
        engine_kwargs={'pool_size': 20, 'pool_recycle': 3600})


@signals.worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global tasks_db_engine, tasks_db_session
    if tasks_db_engine:
        log.debug('Closing database connectionn for the worker')
        tasks_db_engine.dispose()
        if tasks_db_session:
            tasks_db_session.close()


class JobTask(Task):
    """Base class for all job lifetime tasks.

    JobTask tasks should be called with `job_id` in kwargs!
    Otherwise we can't link exceptions and jobs.

    TODO: This class should require job_id somehow.

    """

    # Public

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """This handler is responsible to catch all job exceptions.

        Exceptions should be wrapped into this library exception
        classes so this function will be able to map it to corresponding
        error messages (could be moved to exceptions).

        """

        # Get job id
        job_id = kwargs['job_id']

        # Get error message
        message = 'Inernal Error'
        if isinstance(exc, exceptions.InvalidJobConfiguration):
            message = 'Invalid job configuration'
        elif isinstance(exc, exceptions.InvalidValidationConfiguration):
            message = 'Invalid validation configuration'

        # Compose job update
        params = {
            'job_id': job_id,
            'status': 'error',
            'error': {'message': message},
            'finished': datetime.datetime.utcnow(),
        }

        # Update database
        helpers.update_job(params, _db_session=tasks_db_session)


@app.task(name='goodtablesio.tasks.validate', base=JobTask)
def validate(validation_conf, job_id):
    """Main validation task.

    Args:
        validation_conf (dict): validation configuration

    See `schemas/validation-conf.yml`.

    """

    # Get job
    job = helpers.get_job(job_id, _db_session=tasks_db_session)

    # TODO: job not found
    if job['status'] == 'created':
        params = {
            'job_id': job_id,
            'status': 'running'
        }
        helpers.update_job(params, _db_session=tasks_db_session)

    # Get report
    settings = validation_conf.get('settings', {})
    inspector = Inspector(**settings)
    report = inspector.inspect(validation_conf['files'], preset='tables')

    # Save report
    params = {
        'job_id': job_id,
        'report': report,
        'finished': datetime.datetime.utcnow(),
        'status': 'success' if report['valid'] else 'failure'
    }

    helpers.update_job(params, _db_session=tasks_db_session)

    job.update(params)

    return job
