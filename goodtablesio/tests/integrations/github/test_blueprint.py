import json
from unittest.mock import patch

import pytest

from goodtablesio import models, settings
from goodtablesio.utils.signature import create_signature
from goodtablesio.tests import factories


pytestmark = pytest.mark.usefixtures('session_cleanup')

# TODO: this test should not rely on external HTTP calls to GitHub


# Tests

@patch('goodtablesio.integrations.github.blueprint.set_commit_status')
def test_create_job(set_commit_status, client, celery_app):

    # TODO: refactor to not use actual calls!
    user = factories.User(github_oauth_token=settings.GITHUB_API_TOKEN)
    factories.GithubRepo(name='frictionlessdata/goodtables.io-example',
                         users=[user])

    data = json.dumps({
        'repository': {
            'name': 'goodtables.io-example',
            'owner': {'name': 'frictionlessdata'},
        },
        'head_commit': {'id': 'd5be243487d9882d7f762e7fa04b36b900164a59'},
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
    assert job['finished']
    assert job['status'] == 'failure'
    assert job['report']


def test_api_repo(client):
    user = factories.User(github_oauth_token='token')
    repo = factories.GithubRepo(name='name', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/github/api/repo/%s' % repo.id)
    assert response.status_code == 200
    assert get_response_data(response) == {
        'repo': {'id': repo.id, 'name': repo.name, 'active': repo.active},
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
            {'id': repo1.id, 'name': repo1.name, 'active': repo1.active},
            {'id': repo2.id, 'name': repo2.name, 'active': repo2.active},
        ],
        'syncing': False,
        'error': None,
    }


@patch('goodtablesio.integrations.github.blueprint.activate_hook')
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


@patch('goodtablesio.integrations.github.blueprint.deactivate_hook')
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
