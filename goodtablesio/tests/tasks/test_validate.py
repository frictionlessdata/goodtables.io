import pytest
import datetime
from unittest import mock
from goodtablesio import models, settings
from goodtablesio.tasks.validate import validate
from goodtablesio.tests import factories
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

@mock.patch('goodtables.inspector.Inspector.inspect')
def test_validate(_inspect):

    # We need to save it on the DB so the session used by the tasks can find it
    job = factories.Job(_save_in_db=True)

    mock_report = {'valid': True, 'errors': []}
    _inspect.return_value = mock_report

    validation_conf = {'source': ['file1', 'file2'], 'settings': {}}
    validate(validation_conf, job_id=job.id)

    _inspect.assert_called_with(validation_conf['source'], preset='nested')

    jobs = models.job.find()

    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['report'] == mock_report
    assert isinstance(updated_job['finished'], datetime.datetime)


def test_validate_skip_rows():
    source = 'text://a,b\n1,2\n#comment'
    format = 'csv'

    # Without skip rows
    job = factories.Job()
    conf = {'source': [{'source': source, 'format': format}]}
    job = validate(conf, job_id=job.id)
    assert job['report']['valid'] is False

    # With skip rows
    job = factories.Job()
    conf = {'source': [{'source': source, 'format': format, 'skip_rows': ['#']}]}
    job = validate(conf, job_id=job.id)
    assert job['report']['valid'] is True


def test_validate_more_than_10_tables():

    # We need to save it on the DB so the session used by the tasks can find it
    job = factories.Job()

    validation_conf = {
            'source': [
                {'source': 'http://example.com/file{}'.format(i)} for i in range(12)
            ],
            'settings': {}
    }
    validate(validation_conf, job_id=job.id)

    jobs = models.job.find()
    assert len(jobs[0]['report']['tables']) == 12


def test_validate_more_than_10_tables_no_settings():

    # We need to save it on the DB so the session used by the tasks can find it
    job = factories.Job()

    validation_conf = {
            'source': [
                {'source': 'http://example.com/file{}'.format(i)} for i in range(12)
            ],
    }
    validate(validation_conf, job_id=job.id)

    jobs = models.job.find()
    assert len(jobs[0]['report']['tables']) == 12


def test_validate_more_than_100_tables():

    # We need to save it on the DB so the session used by the tasks can find it
    job = factories.Job()

    validation_conf = {
            'source': [
                {'source': 'http://example.com/file{}'.format(i)} for i in range(110)
            ],
            'settings': {}
    }
    validate(validation_conf, job_id=job.id)

    jobs = models.job.find()
    assert len(jobs[0]['report']['tables']) == settings.MAX_TABLES_PER_SOURCE


def test_validate_more_than_100_tables_even_if_settings():

    # We need to save it on the DB so the session used by the tasks can find it
    job = factories.Job()

    validation_conf = {
            'source': [
                {'source': 'http://example.com/file{}'.format(i)} for i in range(110)
            ],
            'settings': {'table_limit': 200}
    }
    validate(validation_conf, job_id=job.id)

    jobs = models.job.find()
    assert len(jobs[0]['report']['tables']) == settings.MAX_TABLES_PER_SOURCE
