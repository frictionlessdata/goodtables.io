import pytest

from goodtablesio import services
from goodtablesio.app import app


@pytest.fixture()
def db_cleanup():

    services.database['jobs'].delete()

    yield


@pytest.fixture()
def client():

    return app.test_client()
