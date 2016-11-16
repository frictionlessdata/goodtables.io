import uuid
import logging
import datetime
from sqlalchemy.types import DateTime
from .validate import validate_task_desc
from .. import tasks
from .. import services
logger = logging.getLogger(__name__)


# Module API

def create_task(task_desc, task_id=None):
    """Create task.

    Args:
        task_desc (dict): task descriptor
        task_id (str): optional task identifier

    Raises:
        exceptions.InvalidTaskDescriptor

    Returns:
        task_id (str): task identifier

    """

    # Validate task descriptor
    validate_task_desc(task_desc)

    # Get task identifier
    if not task_id:
        task_id = str(uuid.uuid4())

    # Write to database
    insert_task_row(task_id)

    # Create celery task
    result = tasks.validate.apply_async((task_desc,), task_id=task_id)

    return result.id


def insert_task_row(task_id):
    row = {
        'task_id': task_id,
        'created': datetime.datetime.utcnow()
    }
    services.database['reports'].insert(row,
                                        types={'created': DateTime},
                                        ensure=True)
    logger.debug('Saved task "%s" to database', task_id)
    return task_id
