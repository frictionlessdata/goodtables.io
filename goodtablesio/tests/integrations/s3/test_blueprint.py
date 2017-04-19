import json
from unittest import mock

import pytest

from goodtablesio import settings
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.utils.signature import create_signature
from goodtablesio.tests import factories
from goodtablesio.integrations.s3.models.bucket import S3Bucket


pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_s3_home(client):

    job1 = factories.Job(integration_name='s3')
    job2 = factories.Job(integration_name='github')

    response = client.get('/s3/')

    body = response.get_data(as_text=True)

    # TODO: improve when final UI is in place
    assert 'S3' in body
    assert job1.id in body
    assert job2.id not in body


def test_s3_settings_logged_in(client):

    user = factories.User()
    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get('/s3/settings')

    assert response.status_code == 200

    body = response.get_data(as_text=True)

    # TODO: improve when final UI is in place
    assert "const component = 'S3Settings'" in body


def test_s3_settings_not_logged_in(client):

    response = client.get('/s3/settings')

    assert response.status_code == 401


def test_s3_hook_wrong_signature(client):

    response = client.post(
        '/s3/hook', headers={'X-GoodTables-Signature': 'no'})

    assert response.status_code == 400
    body = response.get_data(as_text=True)
    assert 'Wrong signature' in body, body


def test_s3_hook_no_payload(client):

    data = 'aa'
    sig = create_signature(settings.S3_LAMBDA_HOOK_SECRET, data)

    response = client.post(
        '/s3/hook', data=data, headers={'X-GoodTables-Signature': sig})

    assert response.status_code == 400
    body = response.get_data(as_text=True)
    assert 'No payload' in body, body


def test_s3_hook_wrong_payload(client):

    data = {'aa': '2'}
    sig = create_signature(settings.S3_LAMBDA_HOOK_SECRET, json.dumps(data))

    response = client.post(
        '/s3/hook', data=json.dumps(data),
        content_type='application/json',
        headers={'X-GoodTables-Signature': sig})

    assert response.status_code == 400
    body = response.get_data(as_text=True)
    assert 'Wrong payload' in body, body


def test_s3_hook_bucket_does_not_exist(client):

    data = {'Records': [{'s3': {'bucket': {'name': 'test-bucket'}}}]}
    sig = create_signature(settings.S3_LAMBDA_HOOK_SECRET, json.dumps(data))

    response = client.post(
        '/s3/hook', data=json.dumps(data),
        content_type='application/json',
        headers={'X-GoodTables-Signature': sig})

    assert response.status_code == 400
    body = response.get_data(as_text=True)
    assert 'bucket not present' in body, body


@mock.patch('goodtablesio.integrations.s3.blueprint._run_validation')
def test_s3_hook_bucket_success(mock_1, client):

    factories.S3Bucket(name='test-bucket')

    data = {'Records': [{'s3': {'bucket': {'name': 'test-bucket'}}}]}
    sig = create_signature(settings.S3_LAMBDA_HOOK_SECRET, json.dumps(data))

    response = client.post(
        '/s3/hook', data=json.dumps(data),
        content_type='application/json',
        headers={'X-GoodTables-Signature': sig})

    assert response.status_code == 200
    body = response.get_data(as_text=True)

    job_id = json.loads(body)['job_id']

    jobs = database['session'].query(Job).all()

    assert jobs[0].id == job_id


def test_s3_api_bucket(client):
    user = factories.User()
    bucket = factories.S3Bucket(name='name', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/%s' % bucket.id)
    assert response.status_code == 200
    assert get_response_data(response) == {
        'bucket': {
            'id': bucket.id, 'name': bucket.name, 'active': bucket.active,
            'integration_name': 's3'
        },
        'error': None,
    }


def test_s3_api_bucket_not_found(client):
    user = factories.User()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/not-found')
    assert response.status_code == 403


def test_s3_api_bucket_list(client):
    user = factories.User()
    bucket1 = factories.S3Bucket(name='name1', users=[user])
    bucket2 = factories.S3Bucket(name='name2', users=[user])
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket')
    assert response.status_code == 200
    assert get_response_data(response) == {
        'buckets': [
            {'id': bucket1.id, 'name': bucket1.name, 'active': bucket1.active,
             'integration_name': 's3'},
            {'id': bucket2.id, 'name': bucket2.name, 'active': bucket2.active,
             'integration_name': 's3'},
        ],
        'error': None,
    }


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_api_bucket_add(mock_set_up_bucket_on_aws, client):
    user = factories.User()
    mock_set_up_bucket_on_aws.return_value = (True, '')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.post('/s3/api/bucket',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'access-key-id': 'id',
            'secret-access-key': 'key',
            'bucket-name': 'name',
        })
    )
    buckets = database['session'].query(S3Bucket).all()
    mock_set_up_bucket_on_aws.assert_called_with('id', 'key', 'name')
    assert buckets[0].name == 'name'
    assert buckets[0].users[0] == user
    assert get_response_data(response) == {
        'bucket': {
            'id': mock.ANY,
            'name': 'name',
            'active': True,
            'integration_name': 's3'
        },
        'error': None,
    }


def test_s3_api_bucket_add_not_logged_in(client):
    response = client.post('/s3/api/bucket')
    assert response.status_code == 401


def test_s3_api_bucket_add_missing_fields(client):
    user = factories.User()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.post('/s3/api/bucket',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({}))
    assert response.status_code == 200
    assert get_response_data(response) == {
        'bucket': None,
        'error': 'Missing fields',
    }


def test_s3_api_bucket_add_already_exists(client):
    user = factories.User()
    bucket = factories.S3Bucket()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.post('/s3/api/bucket',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'access-key-id': 'test',
            'secret-access-key': 'test',
            'bucket-name': bucket.name
        })
    )
    assert response.status_code == 200
    assert get_response_data(response) == {
        'bucket': None,
        'error': 'Bucket already exists',
    }


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_api_bucket_add_failure(mock_set_up_bucket_on_aws, client):
    user = factories.User()
    mock_set_up_bucket_on_aws.return_value = (False, 'Some error happened')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.post('/s3/api/bucket',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'access-key-id': 'test',
            'secret-access-key': 'test',
            'bucket-name': 'test',
        })
    )
    assert response.status_code == 200
    assert get_response_data(response) == {
        'bucket': None,
        'error': 'Error setting up bucket integration. Some error happened',
    }


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_api_bucket_activate(mock_set_up_bucket_on_aws, client):
    user = factories.User()
    bucket = factories.S3Bucket(
        users=[user], active=False,
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    mock_set_up_bucket_on_aws.return_value = (True, '')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/{}/activate'.format(bucket.id))
    buckets = database['session'].query(S3Bucket).all()
    assert buckets[0].name == bucket.name
    assert buckets[0].active is True
    assert response.status_code == 200
    assert get_response_data(response) == {
        'error': None,
    }


@mock.patch('goodtablesio.integrations.s3.blueprint.disable_bucket_on_aws')
def test_s3_api_bucket_deactivate(mock_disable_bucket_on_aws, client):
    user = factories.User()
    bucket = factories.S3Bucket(
        users=[user], active=True,
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    mock_disable_bucket_on_aws.return_value = (True, '')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/{}/deactivate'.format(bucket.id))
    buckets = database['session'].query(S3Bucket).all()
    assert buckets[0].name == bucket.name
    assert buckets[0].active is False
    assert response.status_code == 200
    assert get_response_data(response) == {
        'error': None,
    }


@mock.patch('goodtablesio.integrations.s3.blueprint.disable_bucket_on_aws')
def test_s3_api_bucket_deactivate_failure(mock_disable_bucket_on_aws, client):
    user = factories.User()
    bucket = factories.S3Bucket(
        users=[user], active=True,
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    mock_disable_bucket_on_aws.return_value = (False, 'Some error happened')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/{}/deactivate'.format(bucket.id))
    assert response.status_code == 200
    assert get_response_data(response) == {
        'error': 'Error removing bucket integration. Some error happened',
    }


def test_s3_api_bucket_deactivate_no_access_to_bucket(client):
    user = factories.User()
    bucket = factories.S3Bucket(
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/{}/deactivate'.format(bucket.id))
    assert response.status_code == 403


def test_s3_api_bucket_deactivate_not_found(client):
    user = factories.User()
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.get('/s3/api/bucket/not-found/deactivate')
    assert response.status_code == 403


@mock.patch('goodtablesio.integrations.s3.blueprint.disable_bucket_on_aws')
def test_s3_api_bucket_delete(mock_disable_bucket_on_aws, client):
    user = factories.User()
    bucket = factories.S3Bucket(
        users=[user], active=True,
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    mock_disable_bucket_on_aws.return_value = (True, '')
    with client.session_transaction() as session:
        session['user_id'] = user.id
    response = client.delete('/s3/api/bucket/{}'.format(bucket.id))
    buckets = database['session'].query(S3Bucket).all()
    assert len(buckets) == 0
    assert response.status_code == 200
    assert get_response_data(response) == {
        'error': None,
    }


# Helpers

def get_response_data(response):
    return json.loads(response.get_data(as_text=True))
