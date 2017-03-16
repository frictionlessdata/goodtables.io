import pytest

from goodtablesio.models.internal_job import InternalJob
from goodtablesio.services import database


pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_create_internal_job_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name',
    }

    database['session'].add(InternalJob(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    job = database['session'].query(InternalJob).get('my-id')

    assert job

    assert job.id == 'my-id'
    assert job.name == 'my-name'
    assert job.status == 'created'
    assert job.created


def test_update_internal_job_stored_in_db():

    params = {
        'id': 'my-id',
        'name': 'my-name',
    }

    database['session'].add(InternalJob(**params))
    database['session'].commit()

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    job = database['session'].query(InternalJob).get('my-id')

    assert job

    job.status = 'success'
    database['session'].add(job)
    database['session'].commit()

    database['session'].remove()

    job = database['session'].query(InternalJob).get('my-id')

    assert job.status == 'success'
