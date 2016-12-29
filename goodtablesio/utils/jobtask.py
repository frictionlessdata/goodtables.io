import datetime
from celery import Task
from goodtablesio import exceptions, models


# Module API

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
        message = 'Internal Error'
        if isinstance(exc, exceptions.InvalidJobConfiguration):
            message = 'Invalid job configuration'
        elif isinstance(exc, exceptions.InvalidValidationConfiguration):
            message = 'Invalid validation configuration'

        # Compose job update
        params = {
            'id': job_id,
            'status': 'error',
            'error': {'message': message},
            'finished': datetime.datetime.utcnow(),
        }

        # Update database
        models.job.update(params)
