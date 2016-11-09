# API hadler stubs (instead of request it gets payload/task_id and returns)
from . import tasks
from . import services


# Module API

def create_task(payload):
    result = tasks.validate.delay(payload)
    return result.id


def get_task(task_id):
    report = None
    result = tasks.validate.AsyncResult(task_id)
    if result.state == 'SUCCESS':
        report = services.database['reports'].find_one(task_id=task_id)
    return {'status': result.status, 'report': report}


def get_task_ids():

    return [r['task_id'] for r in services.database['reports'].all()]
