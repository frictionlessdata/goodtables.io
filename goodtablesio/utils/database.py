import logging
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from goodtablesio import settings
log = logging.getLogger(__name__)


# Module API

def create_session(**params):
    engine = create_engine(settings.DATABASE_URL, **params)
    session = scoped_session(sessionmaker(bind=engine))
    return session


def cleanup_session(session):
    # To prevent session from break because of unhandled error with no rollback
    # https://github.com/frictionlessdata/goodtables.io/issues/97
    # https://github.com/frictionlessdata/goodtables.io/issues/317
    from goodtablesio.models.internal_job import InternalJob
    from goodtablesio.models.job import Job
    log.info('Database session cleanup: rollback and fix stale jobs')
    # Rollback session
    session.rollback()
    # Fix stale jobs
    for model in [Job, InternalJob]:
        utcnow = datetime.datetime.utcnow()
        since = utcnow - datetime.timedelta(seconds=settings.task_soft_time_limit)
        error = {'message': 'Time limit exceeded'}
        (session.query(model)
            .filter(model.finished == None, model.created < since)
            .update({'finished': utcnow, 'status': 'error', 'error': error},
                synchronize_session='fetch'))
        session.commit()
