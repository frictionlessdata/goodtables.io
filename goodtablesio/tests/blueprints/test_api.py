import json
from unittest import mock
import pytest
from goodtablesio import models
from goodtablesio.tests import factories
# Clean up DB on all this module's tests
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_basic(client):

    response = client.get('/api/')

    assert response.status_code == 200
    assert response.content_type == 'application/json; charset=utf-8'


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_job_list_empty(client):

    response = client.get('/api/job')

    assert get_response_data(response) == []


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_job_list(client):

    job1 = factories.Job()
    job2 = factories.Job()

    response = client.get('/api/job')

    assert get_response_data(response) == [job2.id, job1.id]


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_get_job(client):

    job = factories.Job()

    response = client.get('/api/job/{0}'.format(job.id))

    data = get_response_data(response)

    # TODO: Update after #19

    assert 'report' in data
    assert data['id'] == job.id
    assert 'created' in data
    assert 'status' in data


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_get_job_not_found(client):

    response = client.get('/api/job/xxx')

    assert response.status_code == 404

    assert get_response_data(response) == {'message': 'Job not found'}


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_create_job(client):

    payload = {'source': [{'source': 'http://example.com'}]}

    # NB: We can't post the payload directly in `data` as Werkzeug
    # will think that the `files` key are actual uploads

    with mock.patch('goodtablesio.tasks.validate'):
        response = client.post(
            '/api/job',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})

    assert response.status_code == 200

    job_id = response.get_data(as_text=True)
    assert models.job.get(job_id)


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_create_job_empty_body(client):

    response = client.post('/api/job')

    assert response.status_code == 400

    assert get_response_data(response) == {'message': 'Missing configuration'}


# TODO reactivate once API auth is implemented
@pytest.mark.xfail
def test_api_create_job_wrong_params(client):

    payload = {'not_files': [{'source': 'http://example.com'}]}

    response = client.post(
        '/api/job',
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'})

    assert response.status_code == 400

    assert get_response_data(response) == {'message': 'Invalid configuration'}


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
