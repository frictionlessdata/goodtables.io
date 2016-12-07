import uuid
import logging

from .validate import validate_validation_conf
from .. import tasks
from .. import services

from goodtablesio.models import Job


log = logging.getLogger(__name__)


def create_and_run_job(validation_conf, job_id=None):
    """Create a job object in the database and send it to the queue.

    Arguments:
        validation_conf (dict): A dict with the validation configuration.
        job_id (str): Optional id that will be assigned to the new job.

    Raises:
        exceptions.InvalidValidationConfiguration: The validation configuration
            was not valid. See schemas/validation-conf.yml

    Returns:
        job_id (str): The newly created job id

    """

    # Validate validation configuration
    validate_validation_conf(validation_conf)

    # Get job identifier
    if not job_id:
        job_id = str(uuid.uuid4())

    # Write to database
    create_job({'job_id': job_id})

    # Create celery task
    tasks.validate.delay(validation_conf, job_id=job_id)

    return job_id


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
