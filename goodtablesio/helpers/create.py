import uuid
import logging

from .validate import validate_validation_conf
from .. import tasks
from .. import services

from goodtablesio.models import Job


logger = logging.getLogger(__name__)


# Module API

def create_job(validation_conf, job_id=None):
    """Create job.

    Args:
        validation_conf (dict): validation configuration
        job_id (str): optional job identifier

    Raises:
        exceptions.InvalidValidationConfiguration

    Returns:
        job_id (str): job identifier

    """

    # Validate validation configuration
    validate_validation_conf(validation_conf)

    # Get job identifier
    if not job_id:
        job_id = str(uuid.uuid4())

    # Write to database
    insert_job_row(job_id)

    # Create celery task
    tasks.validate.delay(validation_conf, job_id=job_id)

    return job_id


def insert_job_row(job_id, plugin_name='api', plugin_conf=None):
    params = {
        'job_id': job_id,
        'plugin_name': plugin_name,
        'plugin_conf': plugin_conf,
    }

    job = Job(**params)

    services.db_session.add(job)

    services.db_session.commit()

    logger.debug('Saved job "%s" to the database', job_id)
    return job_id
