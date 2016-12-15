import datetime

from celery import Celery, Task
from goodtables import Inspector

from goodtablesio import settings, exceptions, models

# Register signals
import goodtablesio.signals  # noqa


# Module API

app = Celery('tasks')
app.config_from_object(settings)

# TODO: automate
app.autodiscover_tasks(['goodtablesio.plugins.github'])


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


@app.task(name='goodtablesio.tasks.validate', base=JobTask)
def validate(validation_conf, job_id):
    """Main validation task.

    Args:
        validation_conf (dict): validation configuration

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
    settings = validation_conf.get('settings', {})
    inspector = Inspector(**settings)
    report = inspector.inspect(validation_conf['files'], preset='tables')

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
