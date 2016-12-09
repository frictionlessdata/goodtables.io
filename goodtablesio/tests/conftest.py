import pytest

from goodtablesio.services import db_session
from goodtablesio.models.job import Job
from goodtablesio.app import app


@pytest.fixture()
def db_cleanup():

    db_session.query(Job).delete()

    db_session.commit()

    yield


@pytest.fixture()
def client():

    return app.test_client()
