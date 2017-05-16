import pytest
from unittest import mock
from goodtablesio import settings
from goodtablesio.integrations.github.utils.status import set_commit_status


# Tests

def test_set_commit_status_success(mock_post):
    mock_response = mock.MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    tokens = ['my-token']

    r = set_commit_status(
        'success', 'my-org', 'my-repo', 'abcde', 1, tokens)

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token my-token'
    }

    expected_data = {
      'state': 'success',
      'target_url': '{base}/github/my-org/my-repo/jobs/1'.format(
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

    tokens = ['my-token']

    r = set_commit_status(
        'failure', 'my-org', 'my-repo', 'abcde', 1, tokens)

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token my-token'
    }

    expected_data = {
      'state': 'failure',
      'target_url': '{base}/github/my-org/my-repo/jobs/1'.format(
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

    tokens = ['my-token']

    r = set_commit_status(
        'pending', 'my-org', 'my-repo', 'abcde', 1, tokens)

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token my-token'
    }

    expected_data = {
      'state': 'pending',
      'target_url': '{base}/github/my-org/my-repo/jobs/1'.format(
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

    tokens = ['my-token']

    r = set_commit_status(
        'error', 'my-org', 'my-repo', 'abcde', 1, tokens)

    assert r

    expected_url = '{base}/repos/my-org/my-repo/statuses/abcde'.format(
        base=settings.GITHUB_API_BASE,
    )

    expected_headers = {
        'Authorization': 'token my-token'
    }

    expected_data = {
      'state': 'error',
      'target_url': '{base}/github/my-org/my-repo/jobs/1'.format(
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

    tokens = ['my-token']

    r = set_commit_status(
        'success', 'my-org', 'my-repo', 'abcde', 1, tokens)

    assert not r


# Fixtures

@pytest.fixture
def mock_post():
    yield mock.patch('requests.post').start()
    mock.patch.stopall()
