import pytest
from unittest.mock import Mock, patch
from goodtablesio import helpers, exceptions


# Tests

def test_get_ids(services):
    services.database['reports'].find.return_value = [
        {'task_id': 'id1'}, {'task_id': 'id2'}
    ]
    assert helpers.get_task_ids() == ['id1', 'id2']



# Fixtures

@pytest.fixture
def services():
    yield patch('goodtablesio.helpers.retrieve.services').start()
    patch.stopall()
