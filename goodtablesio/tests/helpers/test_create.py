import pytest
from goodtablesio import helpers, exceptions


def test_create_and_run_job_invalid():
    validation_conf = {
        'files': {},
    }
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        assert helpers.create_and_run_job(validation_conf)


@pytest.mark.usefixtures('db_cleanup')
def test_create_job():

    helpers.create_job({'job_id': 'my-id'})

    job = helpers.get_job('my-id')

    assert job['job_id'] == 'my-id'
    assert job['status'] == 'created'
    assert job['plugin_name'] == 'api'
    assert job['plugin_conf'] is None
    assert job['created']
    assert job['finished'] is None
    assert job['report'] is None
    assert job['error'] is None


@pytest.mark.usefixtures('db_cleanup')
def test_create_job_plugin_conf():

    params = {
        'job_id': 'my-id',
        'plugin_name': 'my-plugin',
        'plugin_conf': {'some': 'conf'}
    }
    helpers.create_job(params)

    job = helpers.get_job('my-id')

    assert job['job_id'] == 'my-id'
    assert job['status'] == 'created'
    assert job['plugin_name'] == 'my-plugin'
    assert job['plugin_conf'] == {'some': 'conf'}
    assert job['created']
    assert job['finished'] is None
    assert job['report'] is None
    assert job['error'] is None
