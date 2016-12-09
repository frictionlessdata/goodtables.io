import pytest

from goodtablesio.services import db_session
from goodtablesio.models.job import Job
from goodtablesio.app import app


@pytest.fixture()
def session_cleanup():

    db_session.query(Job).delete()

    yield


@pytest.fixture()
def client():

    return app.test_client()
