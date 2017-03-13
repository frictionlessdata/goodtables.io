import pytest
from goodtablesio.app import app
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.models.plan import Subscription
from goodtablesio.models.source import Source
from goodtablesio.models.integration import Integration
from goodtablesio.celery_app import celery_app as celapp


# Fixture

def pytest_configure(config):

    for integration in ('api', 's3', 'github'):
        if not database['session'].query(Integration).get(integration):
            database['session'].add(Integration(name=integration))


@pytest.fixture()
def session_cleanup():

    database['session'].query(Job).delete()
    database['session'].query(Subscription).delete()
    database['session'].query(User).delete()
    database['session'].query(Source).delete()

    yield


@pytest.fixture()
def client():

    with app.test_client() as c:

        # Save a reference to the app for convenience
        c.app = app

        yield c


@pytest.fixture()
def celery_app():

    # We don't need to restore it because tests
    # always use eager (non forking) mode
    celapp.conf['task_always_eager'] = True

    return celapp
