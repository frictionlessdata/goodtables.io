import uuid
import datetime

from sqlalchemy.types import DateTime

from .. import tasks
from .. import services


# Module API

def create_task(payload, task_id=None):

    # TODO: validate task id if provided
    if not task_id:
        task_id = str(uuid.uuid4())

    row = {
        'task_id': task_id,
        'created': datetime.datetime.utcnow()
    }
    services.database['reports'].insert(row,
                                        types={'created': DateTime},
                                        ensure=True)
    result = tasks.validate.apply_async((payload,), task_id=task_id)
    return result.id


def get_task(task_id):
    report = None
    result = tasks.validate.AsyncResult(task_id)
    if result.state == 'SUCCESS':
        report = services.database['reports'].find_one(task_id=task_id)
    return {'status': result.status, 'report': report}


def get_task_ids():

    return [r['task_id']
            for r in
            services.database['reports'].find(order_by=['-created'])]
