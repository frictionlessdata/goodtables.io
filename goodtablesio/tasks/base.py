import logging
import datetime
from celery import Task
from celery.exceptions import SoftTimeLimitExceeded
from goodtablesio import exceptions
from goodtablesio.models.job import Job
from goodtablesio.services import database
from goodtablesio.models.internal_job import InternalJob
log = logging.getLogger(__name__)


# Module API

class JobTask(Task):
    """Base class for all jobs lifetime celery tasks.

    Any tasks should be called with `job_id` in kwargs!
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
        _on_failure(exc, job_class=Job, job_id=kwargs['job_id'])


class InternalJobTask(Task):
    """Base class for all internal jobs lifetime celery tasks.
    """

    # Public

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        _on_failure(exc, job_class=InternalJob, job_id=kwargs['job_id'])


# Internal

def _on_failure(exception, job_class, job_id):

    # Get error message
    if isinstance(exception, exceptions.InvalidJobConfiguration):
        message = str(exception)
    elif isinstance(exception, exceptions.InvalidValidationConfiguration):
        message = str(exception)
    elif isinstance(exception, SoftTimeLimitExceeded):
        message = 'Time limit exceeded'
    else:
        message = 'Internal error'
        log.exception(exception)

    # Update database
    job = database['session'].query(job_class).get(job_id)
    if job:
        job.status = 'error'
        job.finished = datetime.datetime.utcnow()
        job.error = {'message': message}
        database['session'].commit()
