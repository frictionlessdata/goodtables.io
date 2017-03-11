import pytest

from goodtablesio.models.task import Task
from goodtablesio.tests import factories
from goodtablesio.services import database


pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_create_task_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name',
    }

    database['session'].add(Task(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    task = database['session'].query(Task).get('my-id')

    assert task

    assert task.id == 'my-id'
    assert task.name == 'my-name'
    assert task.status == 'created'
    assert task.created


def test_update_task_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name',
    }

    database['session'].add(Task(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    task = database['session'].query(Task).get('my-id')

    assert task

    task.status = 'success'
    database['session'].add(task)
    database['session'].commit()

    database['session'].remove()

    task = database['session'].query(Task).get('my-id')

    assert task.status == 'success'
