'''
This is the main API that client applications and integrations can use
'''

from goodtablesio.tasks import validate_table, get_task_status


def create_task(url):
    '''
    Given the URL or path to one or more tabular files, plus optional
    configuration options, add a validation task to the queue.

    TODO: Flesh out the parameters

    Returns the task id
    '''
    task = validate_table.delay(url)

    return task.task_id


def get_task(task_id):
    '''
    Returns an object with details for the task provided.

    The object returned has the following keys:

    * id: Task id
    * status: A string describing the status of the actual task (not the
        validation result): eg SUCCESS, PENDING, FAILURE
    * result: The result object returned by the validation task (if any)

    '''
    return get_task_status(task_id)
