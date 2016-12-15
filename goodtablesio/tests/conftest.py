import pytest

from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.tasks import app as celapp
from goodtablesio.app import app


@pytest.fixture()
def session_cleanup():

    database['session'].query(Job).delete()
    database['session'].query(User).delete()

    yield


@pytest.fixture()
def client():

    return app.test_client()


@pytest.fixture()
def celery_app():

    # We don't need to restore it because tests
    # always use eager (non forking) mode
    celapp.conf['task_always_eager'] = True

    return celapp
