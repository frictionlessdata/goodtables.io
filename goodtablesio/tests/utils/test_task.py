import pytest
from celery import Celery
from goodtablesio.utils.task import Task
from goodtablesio.tests import factories
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_Task_on_failure_exception():

    # Prepare things
    task = factories.Task(_save_in_db=True)
    app = Celery('app')
    app.conf['task_always_eager'] = True

    # Prepare and call task
    @app.task(base=Task)
    def task_func():
        raise RuntimeError('bad')
    task_func.apply_async(task_id=task.id)

    # Assert errored task
    assert task.status == 'error'
    assert task.error == {'message': 'bad'}
    assert task.finished
