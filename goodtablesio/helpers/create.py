import uuid
import datetime
from sqlalchemy.types import DateTime
from .validate import validate_validation_conf
from .. import tasks
from .. import services


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
    result = tasks.validate.apply_async((validation_conf,), job_id=job_id)

    return result.id


def insert_job_row(job_id):
    row = {
        'job_id': job_id,
        'created': datetime.datetime.utcnow()
    }
    services.database['reports'].insert(row,
                                        types={'created': DateTime},
                                        ensure=True)
    return job_id
