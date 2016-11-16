from goodtablesio import services


# Module API

def get_task(task_id):
    """Get task by identifier.

    Args:
        task_id (str): task identifier

    Returns:
        dict: task result

    """
    report = services.database['reports'].find_one(task_id=task_id)
    # TODO: we need to store the status in the DB as we can no longer rely on
    # the task id being the same one used by celery
    status = 'Not Implemented'
    return {'status': status, 'report': report}


def get_task_ids():
    """Get all task identifiers.

    Returns:
        str[]: list of task identifiers

    """
    return [r['task_id']
            for r in
            services.database['reports'].find(order_by=['-created'])]
