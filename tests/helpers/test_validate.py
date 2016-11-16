import pytest
from goodtablesio import helpers, exceptions


# Tests

def test_validate_job_conf():
    assert helpers.validate_job_conf({
        'files': '*',
    })


def test_validate_job_conf_invalid():
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert helpers.validate_job_conf({
            'files': ['*'],
        })


def test_validate_validation_conf():
    assert helpers.validate_validation_conf({
        'files': [{'source': 'path.csv'}],
    })


def test_validate_validation_conf_invalid():
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        assert helpers.validate_validation_conf({
            'files': ['*'],
        })
