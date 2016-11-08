import dataset
from celery import Celery
from goodtables import Inspector
from sqlalchemy.dialects.postgresql import JSONB
from . import config


# Module API

app = Celery('tasks')
app.config_from_object(config)


@app.task(name='goodtableio.tasks.validate')
def validate(payload):
    """Main validation task.

    Args:
        payload (mixed): task payload

    """

    # Get report
    inspector = Inspector(**payload.pop('config', {}))
    report = inspector.inspect(**payload)

    # Save report
    # TODO: use shared connection?
    database = dataset.connect(config.DATABASE_URL)
    row = {'task_id': validate.request.id, 'report': report}
    database['reports'].insert(row, types={'report': JSONB}, ensure=True)
