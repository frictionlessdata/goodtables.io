# pylama:skip=1
import json
from unittest.mock import patch
from goodtablesio.tasks import app as celery_app
from goodtablesio.plugins.github.blueprint import _get_owner_repo_sha


# Tests

# High-level test for now fails because of db session error
# @patch('goodtablesio.plugins.github.blueprint.set_commit_status')
# def test_create_job(set_commit_status, client):
    # celery_app.conf['task_always_eager'] = True
    # res = client.post('/github/hook',
        # content_type='application/json',
        # data=json.dumps({
            # 'repository': {
                # 'name': 'goodtables.io-example',
                # 'owner': {'name': 'frictionessdata'},
            # },
            # 'head_commit': {'id': 'd5be243487d9882d7f762e7fa04b36b900164a59'},
        # }
    # ))


def test_get_owner_repo_sha_PUSH():
    payload = {
      'repository': {'name': 'repo', 'owner': {'name': 'owner'}},
      'head_commit': {'id': 'sha'},
    }
    assert _get_owner_repo_sha(payload) == ('owner', 'repo', 'sha')


def test_get_owner_repo_sha_PR():
    payload = {
      'action': 'opened',
      'pull_request': {
          'head': {
              'repo': {'name': 'repo', 'owner': {'login': 'owner'}},
              'sha': 'sha',
          },
       },
    }
    assert _get_owner_repo_sha(payload) == ('owner', 'repo', 'sha')


def test_get_owner_repo_sha_PR_other_action():
    payload = {
      'action': 'labeled',
      'pull_request': {},
    }
    assert _get_owner_repo_sha(payload) == (None, None, None)


def test_get_owner_repo_sha_bad_payload():
    payload = {
      'key': 'value',
    }
    assert _get_owner_repo_sha(payload) == (None, None, None)
