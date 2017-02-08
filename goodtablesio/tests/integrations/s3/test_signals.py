from unittest import mock

from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.tests import factories
from goodtablesio.integrations.s3.signals import post_task_handler


def test_signal_success():

    report = {
        'tables': [
            {'source': 'http://example.com/my_data/some.csv?auth_key=xxx'},
            {'source': 'http://example.com/some%20other.csv?auth_key=xxx'}
        ]
    }

    job = factories.Job(integration_name='s3', report=report, status='success')

    post_task_handler(
        retval=job.to_dict(), state='SUCCESS')

    updated_job = database['session'].query(Job).get(job.id)

    assert updated_job.report == {
        'tables': [
            {'source': 'my_data/some.csv'},
            {'source': 'some other.csv'}
        ]
    }


@mock.patch('goodtablesio.models.job.update')
def test_different_integration(_update):

    job = factories.Job(integration_name='github', status='success')

    post_task_handler(
        retval=job.to_dict(), state='SUCCESS')

    _update.assert_not_called()


@mock.patch('goodtablesio.models.job.update')
def test_signal_exception(_update):

    job = factories.Job(integration_name='s3', status='success')

    post_task_handler(
        retval=Exception(),
        kwargs={'job_id': job.id},
        state='SUCCESS')

    _update.assert_not_called()
