from unittest import mock

import pytest

from goodtablesio import settings
from goodtablesio.plugins.github.utils import set_commit_status
from goodtablesio.plugins.github.utils import create_signature, validate_signature


def test_set_commit_status_success(mock_post):
    mock_response = mock.MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    r = set_commit_status('success', 'my-org', 'my-repo', 'abcde', 'my-job-id')

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token {0}'.format(settings.GITHUB_API_TOKEN),
    }

    expected_data = {
      'state': 'success',
      'target_url': '{base}/job/my-job-id'.format(
           base=settings.BASE_URL),
      'description': 'Data is valid',
      'context': 'goodtables.io/push'
    }

    mock_post.assert_called_with(
        expected_url, json=expected_data, headers=expected_headers)


def test_set_commit_status_failure(mock_post):
    mock_response = mock.MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    r = set_commit_status('failure', 'my-org', 'my-repo', 'abcde', 'my-job-id')

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token {0}'.format(settings.GITHUB_API_TOKEN),
    }

    expected_data = {
      'state': 'failure',
      'target_url': '{base}/job/my-job-id'.format(
           base=settings.BASE_URL),
      'description': 'Data is invalid',
      'context': 'goodtables.io/push'
    }

    mock_post.assert_called_with(
        expected_url, json=expected_data, headers=expected_headers)


def test_set_commit_status_pending(mock_post):
    mock_response = mock.MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    r = set_commit_status('pending', 'my-org', 'my-repo', 'abcde', 'my-job-id')

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token {0}'.format(settings.GITHUB_API_TOKEN),
    }

    expected_data = {
      'state': 'pending',
      'target_url': '{base}/job/my-job-id'.format(
           base=settings.BASE_URL),
      'description': 'Data validation under way',
      'context': 'goodtables.io/push'
    }

    mock_post.assert_called_with(
        expected_url, json=expected_data, headers=expected_headers)


def test_set_commit_status_error(mock_post):
    mock_response = mock.MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    r = set_commit_status('error', 'my-org', 'my-repo', 'abcde', 'my-job-id')

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token {0}'.format(settings.GITHUB_API_TOKEN),
    }

    expected_data = {
      'state': 'error',
      'target_url': '{base}/job/my-job-id'.format(
           base=settings.BASE_URL),
      'description': 'Errors during data validation',
      'context': 'goodtables.io/push'
    }

    mock_post.assert_called_with(
        expected_url, json=expected_data, headers=expected_headers)


def test_set_commit_status_problem(mock_post):
    mock_response = mock.MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    r = set_commit_status('success', 'my-org', 'my-repo', 'abcde', 'my-job-id')

    assert not r


def test_create_signature():
    key = 'key'
    text = 'text'
    signature = 'sha1=369e2959eb49450338b212748f77d8ded74847bb'
    assert create_signature(key, text) == signature


def test_validate_signature():
    key = 'key'
    text = 'text'
    signature = 'sha1=369e2959eb49450338b212748f77d8ded74847bb'
    assert validate_signature(key, text, signature)


def test_validate_signature_invalid():
    key = 'key'
    text = 'text'
    signature = 'sha1=369e2959eb49450338b212748f77d8ded74-----'
    assert not validate_signature(key, text, signature)


@pytest.fixture
def mock_post():
    yield mock.patch('requests.post').start()
    mock.patch.stopall()
