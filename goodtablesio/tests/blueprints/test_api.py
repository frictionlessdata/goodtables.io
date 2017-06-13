# pylama:ignore=W0612
import json
import pytest
from unittest import mock
from goodtablesio.tests import factories
from goodtablesio.models.job import Job
from goodtablesio.models.source import Source
pytestmark = pytest.mark.usefixtures('session_cleanup')


# General endpoints

def test_api_root(get):
    user = factories.User()
    token = user.create_api_token()
    code, data = get('/api/', token=token.token)
    assert code == 200
    assert 'endpoints' in data


def test_api_root_no_token(get):
    code, data = get('/api/')
    assert code == 401
    assert data['message'].startswith('Unauthorized')


def test_api_root_empty_token(get):
    code, data = get('/api/', token='')
    assert code == 401
    assert data['message'].startswith('Unauthorized')


def test_api_root_bad_token(get):
    user = factories.User()
    token = user.create_api_token()
    code, data = get('/api/', token='%s-bad' % token.token)
    assert code == 401
    assert data['message'].startswith('Unauthorized')


def test_api_source_list(get):
    user = factories.User()
    token = user.create_api_token()
    source1 = factories.Source(users=[user], integration_name='github')
    source2 = factories.Source(users=[user], integration_name='api')
    source3 = factories.Source(users=[], integration_name='s3')
    code, data = get('/api/source', token=token.token)
    assert code == 200
    assert len(data['sources']) == 2
    assert data['sources'][0]['id'] == source1.id
    assert data['sources'][0]['name'] == source1.name
    assert data['sources'][1]['id'] == source2.id
    assert data['sources'][1]['name'] == source2.name


def test_api_source_list_empty(get):
    user = factories.User()
    token = user.create_api_token()
    code, data = get('/api/source', token=token.token)
    assert code == 200
    assert data == {'sources': []}


def test_api_source_get(get):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user], integration_name='github')
    code, data = get('/api/source/%s' % source.id, token=token.token)
    assert code == 200
    assert data['source']['id'] == source.id
    assert data['source']['name'] == source.name


def test_api_source_get_own_private(get):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user],
        integration_name='api', conf={'private': True})
    code, data = get('/api/source/%s' % source.id, token=token.token)
    assert code == 200
    assert data['source']['id'] == source.id
    assert data['source']['name'] == source.name


def test_api_source_get_foreign_private(get):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(integration_name='api', conf={'private': True})
    code, data = get('/api/source/%s' % source.id, token=token.token)
    assert code == 403
    assert data['message'] == 'Forbidden'


def test_api_source_get_non_existent(get):
    user = factories.User()
    token = user.create_api_token()
    code, data = get('/api/source/%s' % 'non-existent', token=token.token)
    assert code == 404
    assert data['message'] == 'Not Found'


def test_api_source_create(post):
    user = factories.User()
    token = user.create_api_token()
    # It's OK to have source with the same name for other integration
    other_source = Source.create(name='name', integration_name='github')
    code, data = post('/api/source', {'name': 'name'}, token=token.token)
    source = Source.get(data['source']['id'])
    assert code == 200
    assert source.id == data['source']['id']
    assert source.integration_name == 'api'
    assert source.users == [user]


def test_api_source_create_no_name(post):
    user = factories.User()
    token = user.create_api_token()
    code, data = post('/api/source', {}, token=token.token)
    assert code == 400
    assert data['message'] == 'Source name is required'


def test_api_source_create_duplicate_name(post):
    user = factories.User()
    token = user.create_api_token()
    source = Source.create(name='name', integration_name='api')
    code, data = post('/api/source', {'name': 'name'}, token=token.token)
    assert code == 409
    assert data['message'] == 'Source name is in use'


def test_api_source_job_list(get):
    source = factories.Source(integration_name='api')
    job1 = factories.Job(source=source)
    job2 = factories.Job(source=source)
    user = factories.User()
    token = user.create_api_token()
    code, data = get('/api/source/%s/job' % source.id, token=token.token)
    assert code == 200
    assert data['jobs'][0]['id'] == job2.id
    assert data['jobs'][1]['id'] == job1.id


def test_api_source_job_list_foreign_private_source(get):
    source = factories.Source(integration_name='api', conf={'private': True})
    job1 = factories.Job(source=source)
    job2 = factories.Job(source=source)
    user = factories.User()
    token = user.create_api_token()
    code, data = get('/api/source/%s/job' % source.id, token=token.token)
    assert code == 403
    assert data['message'] == 'Forbidden'


def test_api_source_job_get(get):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user],
        integration_name='api', conf={'private': True})
    job = factories.Job(source=source)
    code, data = get('/api/source/%s/job/%s' % (source.id, job.id), token=token.token)
    assert code == 200
    assert data['job']['id'] == job.id


def test_api_source_job_get_not_found(get):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user], integration_name='api')
    code, data = get('/api/source/%s/job/not-existent' % source.id, token=token.token)
    assert code == 404
    assert data['message'] == 'Not Found'


def test_api_source_job_create(post):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user], integration_name='api')
    payload = {'source': [{'source': 'http://example.com'}]}
    with mock.patch('goodtablesio.tasks.validate'):
        code, data = post('/api/source/%s/job' % source.id, payload, token=token.token)
    job = Job.get(data['job']['id'])
    assert code == 200
    assert job.source == source


def test_api_source_job_create_foreign_private_source(post):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[], integration_name='api', conf={'private': True})
    code, data = post('/api/source/%s/job' % source.id, {}, token=token.token)
    assert code == 403
    assert data['message'] == 'Forbidden'


def test_api_source_job_create_non_api_integration_source(post):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user], integration_name='github')
    code, data = post('/api/source/%s/job' % source.id, {}, token=token.token)
    assert code == 403
    assert data['message'].startswith('Forbidden')


def test_api_source_job_create_empty_body(post):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user], integration_name='api')
    code, data = post('/api/source/%s/job' % source.id, {}, token=token.token)
    assert code == 400
    assert data['message'] == 'Missing configuration'


def test_api_source_job_create_wrong_params(post):
    user = factories.User()
    token = user.create_api_token()
    source = factories.Source(users=[user], integration_name='api')
    payload = {'not_files': [{'source': 'http://example.com'}]}
    code, data = post('/api/source/%s/job' % source.id, payload, token=token.token)
    assert code == 400
    assert data['message'] == 'Invalid configuration'


# Token endpoints

def test_api_token_list(get):
    user = factories.User()
    token1 = user.create_api_token()
    token2 = user.create_api_token()
    with get.client.session_transaction() as session:
        session['user_id'] = user.id
    code, data = get('/api/token')
    assert code == 200
    assert len(data['tokens']) == 2
    assert data['tokens'][0]['id'] == token1.id
    assert data['tokens'][0]['token'] == token1.token
    assert data['tokens'][1]['id'] == token2.id
    assert data['tokens'][1]['token'] == token2.token


def test_api_token_list_not_logged_in(get):
    code, data = get('/api/token')
    assert code == 401
    assert 'authorized' in data['message']


def test_api_token_create(post):
    user = factories.User()
    with post.client.session_transaction() as session:
        session['user_id'] = user.id
    code, data = post('/api/token', {'description': 'description'})
    assert code == 200
    assert data['token']['id'] == user.api_tokens[0].id
    assert data['token']['token'] == user.api_tokens[0].token
    assert code == 200
    assert len(user.api_tokens) == 1


def test_api_token_delete(delete):
    user = factories.User()
    token1 = user.create_api_token()
    token2 = user.create_api_token()
    with delete.client.session_transaction() as session:
        session['user_id'] = user.id
    code, data = delete('/api/token/%s' % token2.id)
    assert code == 200
    assert user.api_tokens == [token1]


# Fixtures

@pytest.fixture
def get(client):
    def func(url, token=None, **params):
        headers = params.pop('headers', {})
        if token is not None:
            headers['Authorization'] = token
        response = client.get(url, headers=headers, **params)
        code = response.status_code
        data = json.loads(response.get_data(as_text=True))
        return code, data
    func.client = client
    return func


@pytest.fixture
def post(client):
    def func(url, payload, token=None, **params):
        headers = params.pop('headers', {})
        if token is not None:
            headers['Authorization'] = token
        headers['Content-Type'] = 'application/json'
        response = client.post(url, data=json.dumps(payload), headers=headers, **params)
        code = response.status_code
        data = json.loads(response.get_data(as_text=True))
        return code, data
    func.client = client
    return func


@pytest.fixture
def delete(client):
    def func(url, token=None, **params):
        headers = params.pop('headers', {})
        if token is not None:
            headers['Authorization'] = token
        response = client.delete(url, headers=headers, **params)
        code = response.status_code
        data = json.loads(response.get_data(as_text=True))
        return code, data
    func.client = client
    return func
