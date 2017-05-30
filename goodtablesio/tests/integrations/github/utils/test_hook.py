import pytest
from unittest.mock import Mock, patch
from goodtablesio import settings
from goodtablesio.integrations.github.utils.hook import (
    activate_hook, deactivate_hook, get_details_from_hook_payload)


# Tests

def test_activate_hook(GitHub):
    activate_hook('token', 'owner', 'repo')
    GitHub.return_value.repository.return_value.create_hook.assert_called_with('web',
        config={
            'secret': settings.GITHUB_HOOK_SECRET,
            'url': settings.GITHUB_HOOK_URL,
            'content_type': 'json',
        }, events=['pull_request', 'push'])


def test_deactivate_hook(GitHub):
    hook1 = Mock(config=Mock(get=Mock(return_value=True)))
    hook2 = Mock(config=Mock(get=Mock(return_value=False)))
    GitHub.return_value.repository.return_value.iter_hooks.return_value = [hook1, hook2]
    deactivate_hook('token', 'owner', 'repo')
    assert hook1.delete.called
    assert not hook2.delete.called


def test_get_details_from_hook_payload_PUSH():
    payload = {
      'ref': 'refs/heads/some-branch',
      'repository': {'name': 'test-repo', 'owner': {'name': 'test-owner'}},
      'head_commit': {
          'id': 'test-sha',
          'message': 'Test message',
          'author': {
              'username': 'test-user',
          }},
    }
    assert get_details_from_hook_payload(payload) == {
        'owner': 'test-owner',
        'repo': 'test-repo',
        'sha': 'test-sha',
        'is_pr': False,
        'commit_message': 'Test message',
        'author_name': 'test-user',
        'branch_name': 'some-branch',
    }


def test_get_details_from_hook_payload_PR():
    payload = {
      'action': 'opened',
      'pull_request': {
          'number': 3,
          'title': 'Test PR',
          'user': {
              'login': 'test-user',
          },
          'head': {
              'repo': {'name': 'test-repo', 'owner': {'login': 'test-owner'}},
              'sha': 'test-sha',
          },
          'base': {
              'repo': {'name': 'test-repo', 'owner': {'login': 'test-owner'}},
          },
       },
    }
    assert get_details_from_hook_payload(payload) == {
        'owner': 'test-owner',
        'repo': 'test-repo',
        'base_owner': 'test-owner',
        'base_repo': 'test-repo',
        'sha': 'test-sha',
        'is_pr': True,
        'pr_number': 3,
        'pr_title': 'Test PR',
        'author_name': 'test-user',
    }


def test_get_details_from_hook_payload_PR_other_fork():
    payload = {
      'action': 'opened',
      'pull_request': {
          'number': 3,
          'title': 'Test PR',
          'user': {
              'login': 'test-user',
          },
          'head': {
              'repo': {'name': 'test-fork-repo', 'owner': {'login': 'test-fork-owner'}},
              'sha': 'test-sha',
          },
          'base': {
              'repo': {'name': 'test-repo', 'owner': {'login': 'test-owner'}},
          }
       },
    }
    assert get_details_from_hook_payload(payload) == {
        'owner': 'test-fork-owner',
        'repo': 'test-fork-repo',
        'base_owner': 'test-owner',
        'base_repo': 'test-repo',
        'sha': 'test-sha',
        'is_pr': True,
        'pr_number': 3,
        'pr_title': 'Test PR',
        'author_name': 'test-user',
    }


def test_get_details_from_hook_payload_PR_other_action():
    payload = {
      'action': 'labeled',
      'pull_request': {'head': {}},
    }
    assert get_details_from_hook_payload(payload) == {}


def test_get_details_from_hook_payload_bad_payload():
    payload = {
      'key': 'value',
    }
    assert get_details_from_hook_payload(payload) is None


# Fixtures

@pytest.fixture
def GitHub():
    GitHub = patch('goodtablesio.integrations.github.utils.hook.GitHub').start()
    yield GitHub
    patch.stopall()
