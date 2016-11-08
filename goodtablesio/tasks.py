from celery import Celery
from goodtables import Inspector
from . import config


app = Celery('tasks')
app.config_from_object(config)


@app.task(name='goodtableio.tasks.validate')
def validate(payload):
    """Main validation task.

    Args:
        payload (mixed): task payload

    """

    inspector = Inspector(**payload.pop('config', {}))
    report = inspector.inspect(**payload)

    # TODO: Upload report
    # task_id = validate.request.id ?

    return report
