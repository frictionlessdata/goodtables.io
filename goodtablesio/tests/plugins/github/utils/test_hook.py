from goodtablesio.plugins.github.utils.hook import get_owner_repo_sha_from_hook_payload


# Tests

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
