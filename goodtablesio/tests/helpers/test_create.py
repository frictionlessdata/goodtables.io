import pytest
from goodtablesio import helpers, exceptions, services


def test_create_job_invalid():
    validation_conf = {
        'files': {},
    }
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        assert helpers.create_job(validation_conf)


@pytest.mark.usefixtures('db_cleanup')
def test_insert_job_row():

    helpers.insert_job_row('my-id')

    job = services.database['jobs'].find_one(job_id='my-id')

    assert job['job_id'] == 'my-id'
    assert job['status'] == 'created'
    assert job['plugin_name'] == 'api'
    assert job['plugin_conf'] is None
    assert job['created']

    # TODO: enable when switching to plain SQLAlchemy
    # assert job['finished'] is None
    # assert job['report'] is None


@pytest.mark.usefixtures('db_cleanup')
def test_insert_job_row_plugin_conf():

    helpers.insert_job_row('my-id', 'my-plugin', {'some': 'conf'})

    job = services.database['jobs'].find_one(job_id='my-id')

    assert job['job_id'] == 'my-id'
    assert job['status'] == 'created'
    assert job['plugin_name'] == 'my-plugin'
    assert job['plugin_conf'] == {'some': 'conf'}
    assert job['created']

    # TODO: enable when switching to plain SQLAlchemy
    # assert job['finished'] is None
    # assert job['report'] is None
