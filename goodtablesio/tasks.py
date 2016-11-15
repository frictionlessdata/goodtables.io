import datetime

import dataset
from celery import Celery
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from goodtables import Inspector


from . import config


# Module API

app = Celery('tasks')
app.config_from_object(config)


@app.task(name='goodtableio.tasks.validate')
def validate(task_desc):
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
        'task_id': validate.request.id,
        'report': report,
        'finished': datetime.datetime.utcnow()
    }
    database['reports'].update(row,
                               ['task_id'],
                               types={'report': JSONB, 'finished': DateTime},
                               ensure=True)
