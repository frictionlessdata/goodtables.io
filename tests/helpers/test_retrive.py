import pytest
from unittest.mock import patch
from goodtablesio import helpers


# Tests

def test_get_ids(services):
    services.database['reports'].find.return_value = [
        {'job_id': 'id1'}, {'job_id': 'id2'}
    ]
    assert helpers.get_job_ids() == ['id1', 'id2']


# Fixtures


@pytest.fixture
def services():
    yield patch('goodtablesio.helpers.retrieve.services').start()
    patch.stopall()
