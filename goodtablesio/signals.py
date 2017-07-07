import os
import logging
import sqlalchemy
from celery import signals
from goodtablesio.utils.database import create_session
from goodtablesio.services import database
log = logging.getLogger(__name__)


# Module API

@signals.worker_process_init.connect
def init_worker(**kwargs):
    log.debug('Initializing database connection for the worker')
    database['session'] = create_session(pool_size=20, pool_recycle=3600)


@signals.worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    database['session'].bind.dispose()
    database['session'].close()


@signals.task_failure.connect
def task_failure(**kwargs):
    exception = kwargs['exception']
    if isinstance(exception, sqlalchemy.exc.SQLAlchemyError):
        # To prevent session from break because of unhandled error with no rollback
        # https://github.com/frictionlessdata/goodtables.io/issues/97
        log.info('Database session rollback by celery error handler')
        database['session'].rollback()


@signals.task_postrun.connect
def task_postrun(**kwargs):
    files = kwargs['kwargs'].get('files')
    if files:
        for path in files.values():
            os.remove(path)
        os.rmdir(os.path.dirname(path))
