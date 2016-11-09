import os

from celery import Celery
from celery.result import AsyncResult

from goodtables import Inspector


app = Celery('tasks')
app.config_from_object('celeryconfig')

for key in ('BROKER_URL', 'RESULT_BACKEND'):
    if key in os.environ:
        app.conf.update({key.lower(): os.environ[key]})


@app.task(name='goodtableio.tasks.validate_table')
def validate_table(url):
    '''
    Main validation task

    TODO: Document
    '''

    # TODO: Process multiple files in batch
    # TODO: Configure inspector (schemas, checks, etc)

    inspector = Inspector()
    report = inspector.inspect(url)

    # TODO: Upload report

    return report


def get_task_status(task_id):
    '''
    Returns an object with details for the task provided.

    TODO: Distinguish between PENDING tasks and not found ones (we probably
    need to store the task id externally)

    The object returned has the following keys:

    * id: Task id
    * status: A string describing the status of the actual task (not the
        validation result): eg SUCCESS, PENDING, FAILURE
    * result: The result object returned by the validation task (if any)

    '''

    res = AsyncResult(task_id)
    return {'status': res.status,
            'id': res.task_id,
            'result': res.result}
