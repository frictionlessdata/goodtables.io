import pytest

from goodtablesio.app import app


@pytest.fixture()
def client():

    return app.test_client()
