import logging
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
