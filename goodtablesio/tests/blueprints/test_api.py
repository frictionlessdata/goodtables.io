import json
import pytest
from unittest import mock
from goodtablesio import models
from goodtablesio.tests import factories
pytestmark = pytest.mark.usefixtures('session_cleanup')


# General endpoints

def test_api_root(client):
    user = factories.User()
    token = user.create_api_token()
    response = client.get('/api/', headers={'Authorization': token.token})
    data = get_response_data(response)
    assert response.status_code == 200
    assert 'endpoints' in data


def test_api_root_no_token(client):
    response = client.get('/api/')
    data = get_response_data(response)
    assert response.status_code == 401
    assert data['message'] == 'Unauthorized'


def test_api_root_empty_token(client):
    response = client.get('/api/', headers={'Authorization': ''})
    data = get_response_data(response)
    assert response.status_code == 401
    assert data['message'] == 'Unauthorized'


def test_api_root_bad_token(client):
    user = factories.User()
    token = user.create_api_token()
    response = client.get('/api/', headers={'Authorization': '%s-bad' % token.token})
    data = get_response_data(response)
    assert response.status_code == 401
    assert data['message'] == 'Unauthorized'


def test_api_job_list_empty(client):
    user = factories.User()
    token = user.create_api_token()
    response = client.get('/api/job', headers={'Authorization': token.token})
    data = get_response_data(response)
    assert data == []


def test_api_job_list(client):
    job1 = factories.Job()
    job2 = factories.Job()
    user = factories.User()
    token = user.create_api_token()
    response = client.get('/api/job', headers={'Authorization': token.token})
    data = get_response_data(response)
    assert data == [job2.id, job1.id]


def test_api_job_get(client):
    job = factories.Job()
    user = factories.User()
    token = user.create_api_token()
    response = client.get('/api/job/%s' % job.id, headers={'Authorization': token.token})
    data = get_response_data(response)
    assert 'report' in data
    assert data['id'] == job.id
    assert 'created' in data
    assert 'status' in data


def test_api_job_get_not_found(client):
    user = factories.User()
    token = user.create_api_token()
    response = client.get('/api/job/xxx', headers={'Authorization': token.token})
    data = get_response_data(response)
    assert response.status_code == 404
    assert data == {'message': 'Job not found'}


def test_api_job_create(client):
    user = factories.User()
    token = user.create_api_token()
    payload = {'source': [{'source': 'http://example.com'}]}
    with mock.patch('goodtablesio.tasks.validate'):
        # NB: We can't post the payload directly in `data` as Werkzeug
        # will think that the `files` key are actual uploads
        response = client.post(
            '/api/job',
            data=json.dumps(payload),
            headers={
                'Authorization': token.token,
                'Content-Type': 'application/json'
            })
    job_id = response.get_data(as_text=True)
    assert response.status_code == 200
    assert models.job.get(job_id)


def test_api_job_create_empty_body(client):
    user = factories.User()
    token = user.create_api_token()
    response = client.post('/api/job', headers={'Authorization': token.token})
    data = get_response_data(response)
    assert response.status_code == 400
    assert data == {'message': 'Missing configuration'}


def test_api_job_create_wrong_params(client):
    user = factories.User()
    token = user.create_api_token()
    payload = {'not_files': [{'source': 'http://example.com'}]}
    response = client.post(
        '/api/job',
        data=json.dumps(payload),
        headers={
            'Authorization': token.token,
            'Content-Type': 'application/json'
        })
    data = get_response_data(response)
    assert response.status_code == 400
    assert data == {'message': 'Invalid configuration'}


# Token endpoints

def test_api_token_list(client):
    user = factories.User()
    token1 = user.create_api_token()
    token2 = user.create_api_token()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/api/token')
    data = get_response_data(response)
    assert len(data['tokens']) == 2
    assert data['tokens'][0]['id'] == token1.id
    assert data['tokens'][0]['token'] == token1.token
    assert data['tokens'][1]['id'] == token2.id
    assert data['tokens'][1]['token'] == token2.token


def test_api_token_list_not_logged_in(client):
    response = client.get('/api/token')
    data = get_response_data(response)
    assert data['status'] == 401


def test_api_token_create(client):
    user = factories.User()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.post(
        '/api/token',
        data=json.dumps({'description': 'description'}),
        headers={'Content-Type': 'application/json'})
    data = get_response_data(response)
    assert data['token']['id'] == user.api_tokens[0].id
    assert data['token']['token'] == user.api_tokens[0].token
    assert len(user.api_tokens) == 1


def test_api_token_delete(client):
    user = factories.User()
    token1 = user.create_api_token()
    token2 = user.create_api_token()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.delete('/api/token/%s' % token2.id)
    get_response_data(response)
    assert user.api_tokens == [token1]


# Helpers

def get_response_data(response):
    return json.loads(response.get_data(as_text=True))
