import pytest
from goodtablesio import helpers, exceptions


# Tests

def test_validate_task_conf():
    assert helpers.validate_task_conf({
        'files': '*',
    })


def test_validate_task_conf_invalid():
    with pytest.raises(exceptions.InvalidTaskConfiguration):
        assert helpers.validate_task_conf({
            'files': ['*'],
        })


def test_validate_task_desc():
    assert helpers.validate_task_desc({
        'files': [{'source': 'path.csv'}],
    })


def test_validate_task_desc_invalid():
    with pytest.raises(exceptions.InvalidTaskDescriptor):
        assert helpers.validate_task_desc({
            'files': ['*'],
        })
