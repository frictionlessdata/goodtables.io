import pytest

from goodtablesio.services import db_session
from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.app import app


@pytest.fixture()
def session_cleanup():

    db_session.query(Job).delete()
    db_session.query(User).delete()

    yield


@pytest.fixture()
def client():

    return app.test_client()
