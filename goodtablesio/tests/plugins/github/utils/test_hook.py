import pytest
from unittest.mock import Mock, patch
from goodtablesio import settings
from goodtablesio.plugins.github.utils.hook import (
    activate_hook, deactivate_hook, get_owner_repo_sha_from_hook_payload)


# Tests

def test_activate_hook(GitHub):
    activate_hook('token', 'owner', 'repo')
    GitHub.return_value.repository.return_value.create_hook.assert_called_with('web',
        config={
            'secret': settings.GITHUB_HOOK_SECRET,
            'url': '%s/github/hook' % settings.BASE_URL,
            'content_type': 'json',
            'is_goodtables_hook': True,
        }, events=['pull_request', 'push'])


def test_deactivate_hook(GitHub):
    hook1 = Mock(config=Mock(get=Mock(return_value=True)))
    hook2 = Mock(config=Mock(get=Mock(return_value=False)))
    GitHub.return_value.repository.return_value.iter_hooks.return_value = [hook1, hook2]
    deactivate_hook('token', 'owner', 'repo')
    assert hook1.delete.called
    assert not hook2.delete.called


def test_get_owner_repo_sha_from_hook_payload_PUSH():
    payload = {
      'repository': {'name': 'repo', 'owner': {'name': 'owner'}},
      'head_commit': {'id': 'sha'},
    }
    assert get_owner_repo_sha_from_hook_payload(payload) == ('owner', 'repo', 'sha')


def test_get_owner_repo_sha_from_hook_payload_PR():
    payload = {
      'action': 'opened',
      'pull_request': {
          'head': {
              'repo': {'name': 'repo', 'owner': {'login': 'owner'}},
              'sha': 'sha',
          },
       },
    }
    assert get_owner_repo_sha_from_hook_payload(payload) == ('owner', 'repo', 'sha')


def test_get_owner_repo_sha_from_hook_payload_PR_other_action():
    payload = {
      'action': 'labeled',
      'pull_request': {},
    }
    assert get_owner_repo_sha_from_hook_payload(payload) == (None, None, None)


def test_get_owner_repo_sha_from_hook_payload_bad_payload():
    payload = {
      'key': 'value',
    }
    assert get_owner_repo_sha_from_hook_payload(payload) == (None, None, None)


# Fixtures

@pytest.fixture
def GitHub():
    GitHub = patch('goodtablesio.plugins.github.utils.hook.GitHub').start()
    yield GitHub
    patch.stopall()
