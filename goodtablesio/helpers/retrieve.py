from .. import tasks
from .. import services


# Module API

def get_task(task_id):
    """Get task by identifier.

    Args:
        task_id (str): task identifier

    Returns:
        dict: task result

    """
    report = None
    result = tasks.validate.AsyncResult(task_id)
    if result.state == 'SUCCESS':
        report = services.database['reports'].find_one(task_id=task_id)
    return {'status': result.status, 'report': report}


def get_task_ids():
    """Get all task identifiers.

    Returns:
        str[]: list of task identifiers

    """
    return [r['task_id']
            for r in
            services.database['reports'].find(order_by=['-created'])]
