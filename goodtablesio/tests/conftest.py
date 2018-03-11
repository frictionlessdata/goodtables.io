import pytest
import os
from goodtablesio.app import app
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.models.internal_job import InternalJob
from goodtablesio.models.user import User
from goodtablesio.models.subscription import Subscription
from goodtablesio.models.source import Source
from goodtablesio.models.integration import Integration
from goodtablesio.celery_app import celery_app as celapp


# Fixture

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


def pytest_configure(config):

    for integration in ('api', 's3', 'github'):
        if not database['session'].query(Integration).get(integration):
            database['session'].add(Integration(name=integration))


@pytest.fixture()
def session_cleanup():

    database['session'].query(Job).delete()
    database['session'].query(InternalJob).delete()
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


@pytest.fixture()
def sample_datapackage():
    path = os.path.join(FIXTURES_PATH, 'datapackage.json')
    yield open(path, 'rb')


@pytest.fixture()
def sample_datapackage_zip():
    path = os.path.join(FIXTURES_PATH, 'sample_datapackage.zip')
    yield open(path, 'rb')


@pytest.fixture()
def sample_csv():
    path = os.path.join(FIXTURES_PATH, 'data.csv')
    yield open(path, 'rb')


@pytest.fixture()
def sample_tableschema():
    path = os.path.join(FIXTURES_PATH, 'schema.json')
    yield open(path, 'rb')
