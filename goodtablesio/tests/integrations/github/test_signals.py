from unittest import mock

from goodtablesio.tests import factories
from goodtablesio.integrations.github.signals import post_task_handler


@mock.patch('goodtablesio.integrations.github.signals.set_commit_status')
@mock.patch('goodtablesio.integrations.github.signals.get_tokens_for_job')
def test_signal_sets_status(get_tokens_for_job, set_commit_status):

    get_tokens_for_job.return_value = ['a', 'b']

    conf = {
        'owner': 'test-org',
        'repo': 'test-repo',
        'sha': 'abcde',
        'is_pr': True
    }

    job = factories.Job(
        integration_name='github', conf=conf, status='success', number=3)

    post_task_handler(
            retval=job.to_dict(), kwargs={'job_id': job.id}, state='SUCCESS')

    set_commit_status.assert_called_with(
        'success',
        owner='test-org',
        repo='test-repo',
        sha='abcde',
        is_pr=True,
        job_number=3,
        tokens=['a', 'b'],
    )


@mock.patch('goodtablesio.integrations.github.signals.set_commit_status')
@mock.patch('goodtablesio.integrations.github.signals.get_tokens_for_job')
def test_signal_no_github(get_tokens_for_job, set_commit_status):

    job = factories.Job(
        integration_name='s3')

    post_task_handler(
            retval=job.to_dict(), kwargs={'job_id': job.id}, state='SUCCESS')

    assert not get_tokens_for_job.called
    assert not set_commit_status.called


@mock.patch('goodtablesio.integrations.github.signals.set_commit_status')
@mock.patch('goodtablesio.integrations.github.signals.get_tokens_for_job')
def test_signal_sets_status_task_error(get_tokens_for_job, set_commit_status):

    get_tokens_for_job.return_value = ['a', 'b']

    conf = {
        'owner': 'test-org',
        'repo': 'test-repo',
        'sha': 'abcde',
        'is_pr': True
    }

    job = factories.Job(
        integration_name='github', conf=conf, number=3)

    post_task_handler(
            retval=job.to_dict(), kwargs={'job_id': job.id}, state='ERROR')

    set_commit_status.assert_called_with(
        'error',
        owner='test-org',
        repo='test-repo',
        sha='abcde',
        is_pr=True,
        job_number=3,
        tokens=['a', 'b'],
    )
