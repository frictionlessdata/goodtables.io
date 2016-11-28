import pytest
from goodtablesio import helpers, exceptions


# Tests

def test_create_job_invalid():
    validation_conf = {
        'files': {},
    }
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        assert helpers.create_job(validation_conf)
