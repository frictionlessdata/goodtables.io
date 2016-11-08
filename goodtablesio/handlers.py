# API hadler stubs (instead of request it gets payload/task_id and returns)
import dataset
from . import tasks
from . import services


# Module API

def post_task(payload):
    result = tasks.validate.delay(payload)
    return result.id


def get_task(task_id):
    report = None
    result = tasks.validate.AsyncResult(task_id)
    if result.state == 'SUCCESS':
        report = services.database['reports'].find_one(task_id=task_id)
    return {'status': result.status, 'report': report}
