import datetime
import logging

import dataset
from celery import Celery
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from goodtables import Inspector

from . import config


log = logging.getLogger(__name__)


# Module API

app = Celery('tasks')
app.config_from_object(config)

# TODO: automate
app.autodiscover_tasks(['goodtablesio.plugins.github'])


@app.task(name='goodtablesio.tasks.validate')
def validate(task_desc, task_id=None):
    """Main validation task.

    Args:
        task_desc (dict): task descriptor

    See `schemas/task-desc.yml`.

    """
    # Get report
    inspector = Inspector(**task_desc['settings'])
    report = inspector.inspect(task_desc['files'], preset='tables')

    # Save report
    database = dataset.connect(config.DATABASE_URL)
    row = {
        'task_id': task_id or validate.request.id,
        'report': report,
        'finished': datetime.datetime.utcnow()
    }
    database['reports'].update(row,
                               ['task_id'],
                               types={'report': JSONB, 'finished': DateTime},
                               ensure=True)
