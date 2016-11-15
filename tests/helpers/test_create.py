import pytest
from goodtablesio import helpers, exceptions


# Tests

def test_create_task_invalid():
    task_desc = {
        'files': {},
    }
    with pytest.raises(exceptions.InvalidTaskDescriptor):
        assert helpers.create_task(task_desc)
