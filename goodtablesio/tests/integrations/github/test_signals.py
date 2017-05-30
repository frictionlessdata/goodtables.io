from unittest import mock

from goodtablesio.tests import factories
from goodtablesio.integrations.github.signals import post_task_handler


@mock.patch('goodtablesio.integrations.github.signals.set_commit_status')
def test_signal_sets_status(set_commit_status):

    conf = {
        'owner': 'test-org',
        'repo': 'test-repo',
        'sha': 'abcde',
        'is_pr': True
    }
    integration = factories.Integration()
    repo = factories.GithubRepo(integration_name=integration.name)
    job = factories.Job(
        integration_name='github', conf=conf, status='success', number=3, source=repo)

    post_task_handler(
            retval=job.to_dict(), kwargs={'job_id': job.id}, state='SUCCESS')

    set_commit_status.assert_called_with(
        'success',
        owner='test-org',
        repo='test-repo',
        sha='abcde',
        is_pr=True,
        job_number=3,
        tokens=job.source.tokens,
    )


@mock.patch('goodtablesio.integrations.github.signals.set_commit_status')
def test_signal_no_github(set_commit_status):

    job = factories.Job(
        integration_name='s3')

    post_task_handler(
            retval=job.to_dict(), kwargs={'job_id': job.id}, state='SUCCESS')

    assert not set_commit_status.called


@mock.patch('goodtablesio.integrations.github.signals.set_commit_status')
def test_signal_sets_status_task_error(set_commit_status):

    conf = {
        'owner': 'test-org',
        'repo': 'test-repo',
        'sha': 'abcde',
        'is_pr': True
    }

    integration = factories.Integration()
    repo = factories.GithubRepo(integration_name=integration.name)
    job = factories.Job(
        integration_name='github', conf=conf, number=3, source=repo)

    post_task_handler(
            retval=job.to_dict(), kwargs={'job_id': job.id}, state='ERROR')

    set_commit_status.assert_called_with(
        'error',
        owner='test-org',
        repo='test-repo',
        sha='abcde',
        is_pr=True,
        job_number=3,
        tokens=job.source.tokens,
    )
