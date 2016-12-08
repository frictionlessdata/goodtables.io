import logging

from .. import services

from goodtablesio.models import Job


log = logging.getLogger(__name__)


def create_job(params, _db_session=None):
    """
    Creates a job object in the database.

    Arguments:
        params (dict): A dictionary with the values for the new job.
        _db_session (Session): An alternative SQLAlchemy session instance. If
            not provided the default one from goodtablesio.services will be
            used. This is useful for tasks run on the Celery processes.

    Returns:
        job_id (str): The newly created job id
    """

    job = Job(**params)

    services.db_session.add(job)
    services.db_session.commit()

    log.debug('Saved job "%s" to the database', job.job_id)
    return job.job_id
