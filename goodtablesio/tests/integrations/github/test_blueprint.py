import json
from unittest import mock

import pytest

from goodtablesio import models, settings
from goodtablesio.utils.signature import create_signature
from goodtablesio.tests import factories


pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests
@mock.patch('goodtablesio.integrations.github.blueprint._run_validation')
@mock.patch('goodtablesio.integrations.github.blueprint.set_commit_status')
def test_create_job_push(run_validation, set_commit_status, client):

    user = factories.User(github_oauth_token='xxx')
    factories.GithubRepo(name='test-org/example',
                         users=[user])

    data = json.dumps({
        'ref': 'refs/head/some-branch',
        'repository': {
            'name': 'example',
            'owner': {'name': 'test-org'},
        },
        'head_commit': {
            'id': 'xxx',
            'message': 'Test commit', 'author': {'username': 'test-user'}},
    })
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)
    job_id = get_response_data(response)['job_id']
    job = models.job.get(job_id)
    assert job['id'] == job_id
    assert job['created']
    assert job['status'] == 'created'


@mock.patch('goodtablesio.integrations.github.blueprint._run_validation')
@mock.patch('goodtablesio.integrations.github.blueprint.set_commit_status')
def test_create_job_pr(run_validation, set_commit_status, client):

    user = factories.User(github_oauth_token='xxx')
    factories.GithubRepo(name='test-org/example',
                         users=[user])

    data = json.dumps({
      'action': 'opened',
      'pull_request': {
          'number': 3,
          'title': 'Test PR',
          'user': {
              'login': 'test-user',
          },

          'head': {
              'repo': {'name': 'example', 'owner': {'login': 'test-org'}},
              'sha': 'test-sha',
          },
          'base': {
              'repo': {'name': 'example', 'owner': {'login': 'test-org'}},
          }
       },
    })
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)
    job_id = get_response_data(response)['job_id']
    job = models.job.get(job_id)
    assert job['id'] == job_id
    assert job['created']
    assert job['status'] == 'created'


def test_create_job_pr_other_action(client):

    user = factories.User(github_oauth_token='xxx')
    source = factories.GithubRepo(name='test-org/example',
                                  users=[user])

    data = json.dumps({
      'action': 'labeled',
      'pull_request': {
          'number': 3,
          'title': 'Test PR',
          'user': {
              'login': 'test-user',
          },

          'head': {
              'repo': {'name': 'example', 'owner': {'login': 'test-org'}},
              'sha': 'test-sha',
          },
          'base': {
              'repo': {'name': 'example', 'owner': {'login': 'test-org'}},
          }
       },
    })
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)

    assert response.status_code == 200
    assert len(source.jobs) == 0


@mock.patch('goodtablesio.integrations.github.blueprint._run_validation')
@mock.patch('goodtablesio.integrations.github.blueprint.set_commit_status')
def test_create_job_pr_from_fork(run_validation, set_commit_status, client):

    user = factories.User(github_oauth_token='xxx')
    factories.GithubRepo(name='test-org/example',
                         users=[user])

    data = json.dumps({
      'action': 'opened',
      'pull_request': {
          'number': 3,
          'title': 'Test PR',
          'user': {
              'login': 'test-user',
          },
          'head': {
              'repo': {'name': 'example', 'owner': {'login': 'different-org'}},
              'sha': 'test-sha',
          },
          'base': {
              'repo': {'name': 'example', 'owner': {'login': 'test-org'}},
          }
       },
    })
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)
    job_id = get_response_data(response)['job_id']
    job = models.job.get(job_id)
    assert job['id'] == job_id
    assert job['created']
    assert job['status'] == 'created'


def test_create_job_wrong_signature(client):

    signature = 'xxx'
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data={})

    assert response.status_code == 400


def test_create_job_no_payload(client):

    data = ''
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)

    assert response.status_code == 400


def test_create_job_wrong_payload(client):

    data = 'xxx'
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)

    assert response.status_code == 400


def test_create_job_source_does_not_exist(client):

    data = json.dumps({
        'repository': {
            'name': 'example',
            'owner': {'name': 'some-org'},
        },
        'head_commit': {'id': 'xxx'},
    })
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)

    assert response.status_code == 400


def test_create_job_wrong_json(client):

    data = json.dumps({'x': 'y'})
    signature = create_signature(settings.GITHUB_HOOK_SECRET, data)
    response = client.post(
        '/github/hook',
        headers={'X-Hub-Signature': signature},
        content_type='application/json',
        data=data)

    assert response.status_code == 400


def test_api_repo(client):
    user = factories.User(github_oauth_token='token')
    repo = factories.GithubRepo(name='name', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/github/api/repo/%s' % repo.id)
    assert response.status_code == 200
    assert get_response_data(response) == {
        'repo': {'id': repo.id, 'name': repo.name, 'active': repo.active,
                 'integration_name': 'github'},
        'error': None,
    }


def test_api_repo_not_authorized(client):
    user = factories.User(github_oauth_token='token')
    repo = factories.GithubRepo(name='name', users=[user])
    response = client.get('/github/api/repo/%s' % repo.id)
    assert response.status_code == 401


def test_api_repo_not_found(client):
    user = factories.User(github_oauth_token='token')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/github/api/repo/not-found')
    assert response.status_code == 403


def test_api_repo_list(client):
    user = factories.User(github_oauth_token='token')
    repo1 = factories.GithubRepo(name='name1', users=[user])
    repo2 = factories.GithubRepo(name='name2', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/github/api/repo')
    assert response.status_code == 200
    assert get_response_data(response) == {
        'repos': [
            {'id': repo1.id, 'name': repo1.name, 'active': repo1.active,
             'integration_name': 'github'},
            {'id': repo2.id, 'name': repo2.name, 'active': repo2.active,
             'integration_name': 'github'},
        ],
        'syncing': False,
        'error': None,
    }


@mock.patch('goodtablesio.integrations.github.blueprint.activate_hook')
def test_api_repo_activate(activate_hook, client):
    user = factories.User(github_oauth_token='token')
    repo = factories.GithubRepo(name='owner/repo', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/github/api/repo/%s/activate' % repo.id)
    activate_hook.assert_called_with('token', 'owner', 'repo')
    assert response.status_code == 200
    assert get_response_data(response) == {
        'error': None,
    }


@mock.patch('goodtablesio.integrations.github.blueprint.deactivate_hook')
def test_api_repo_deactivate(deactivate_hook, client):
    user = factories.User(github_oauth_token='token')
    repo = factories.GithubRepo(name='owner/repo', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/github/api/repo/%s/deactivate' % repo.id)
    deactivate_hook.assert_called_with('token', 'owner', 'repo')
    assert response.status_code == 200
    assert get_response_data(response) == {
        'error': None,
    }


# Helpers

def get_response_data(response):
    return json.loads(response.get_data(as_text=True))
