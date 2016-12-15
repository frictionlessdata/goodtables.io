import json
from unittest.mock import patch
from goodtablesio import models, settings
from goodtablesio.plugins.github.blueprint import _get_owner_repo_sha
from goodtablesio.plugins.github.utils import create_signature


# Tests

@patch('goodtablesio.plugins.github.blueprint.set_commit_status')
def test_create_job(set_commit_status, client, celery_app):
    data = json.dumps({
        'repository': {
            'name': 'goodtables.io-example',
            'owner': {'name': 'frictionlessdata'},
        },
        'head_commit': {'id': 'd5be243487d9882d7f762e7fa04b36b900164a59'},
    })
    sig = create_signature(settings.GITHUB_HOOK_SECRET, data)
    res = client.post('/github/hook',
        headers={'HTTP_X_HUB_SIGNATURE': sig},
        content_type='application/json',
        data=data)
    job_id = json.loads(res.get_data(as_text=True))['job_id']
    job = models.job.get(job_id)
    assert job['id'] == job_id
    assert job['created']
    assert job['finished']
    assert job['status'] == 'failure'
    assert job['report']


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


# Helpers

def _get_json(response):
    return json.loads(response.get_data(as_text=True))
