<<<<<<< HEAD
import json
=======
# pylama:skip=1
>>>>>>> fixed tests, badge
from unittest import mock

import pytest

from goodtablesio import settings
from goodtablesio.services import database
from goodtablesio.models.job import Job
from goodtablesio.utils.signature import create_signature
from goodtablesio.tests import factories
from goodtablesio.integrations.s3.models.bucket import S3Bucket


pytestmark = pytest.mark.usefixtures('session_cleanup')


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
    # assert 'Add Bucket' in body


def test_s3_settings_not_logged_in(client):

    response = client.get('/s3/settings')

    assert response.status_code == 401


def test_s3_settings_add_bucket_not_logged_in(client):

    response = client.post('/s3/settings/add_bucket')

    assert response.status_code == 401


def test_s3_settings_add_bucket_get(client):

    response = client.get('/s3/settings/add_bucket')

    assert response.status_code == 405


def test_s3_settings_add_bucket_missing_params(client):

    user = factories.User()
    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.post(
        '/s3/settings/add_bucket', follow_redirects=True)

    # TODO: improve when final UI is in place
    # assert 'Missing fields' in response.get_data(as_text=True)


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_settings_add_bucket_success(mock_set_up_bucket_on_aws, client):

    mock_set_up_bucket_on_aws.return_value = (True, '')

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    data = {
        'access-key-id': 'test',
        'secret-access-key': 'test',
        'bucket-name': 'test'
    }
    response = client.post(
        '/s3/settings/add_bucket', data=data, follow_redirects=True)

    # TODO: improve when final UI is in place
    # body = response.get_data(as_text=True)
    # assert 'Bucket added' in body, body

    buckets = database['session'].query(S3Bucket).all()

    assert buckets[0].name == 'test'
    assert buckets[0].users[0] == user


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_settings_add_bucket_success_redirects(
     mock_set_up_bucket_on_aws, client):

    mock_set_up_bucket_on_aws.return_value = (True, '')

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    data = {
        'access-key-id': 'test',
        'secret-access-key': 'test',
        'bucket-name': 'test'
    }
    response = client.post(
        '/s3/settings/add_bucket', data=data)

    assert response.status_code == 302
    assert response.location == 'http://localhost/s3/settings'


def test_s3_settings_add_bucket_already_exists(client):

    bucket = factories.S3Bucket()
    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    data = {
        'access-key-id': 'test',
        'secret-access-key': 'test',
        'bucket-name': bucket.name
    }
    response = client.post(
        '/s3/settings/add_bucket', data=data, follow_redirects=True)

    # TODO: improve when final UI is in place
    # body = response.get_data(as_text=True)
    # assert 'Bucket already exists' in body, body


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_settings_add_bucket_failure(mock_set_up_bucket_on_aws, client):

    mock_set_up_bucket_on_aws.return_value = (False, 'Some error happened')

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    data = {
        'access-key-id': 'test',
        'secret-access-key': 'test',
        'bucket-name': 'test'
    }
    response = client.post(
        '/s3/settings/add_bucket', data=data, follow_redirects=True)

    # TODO: improve when final UI is in place
    # body = response.get_data(as_text=True)
    # assert 'Some error happened' in body, body


@mock.patch('goodtablesio.integrations.s3.blueprint.set_up_bucket_on_aws')
def test_s3_settings_add_bucket_failure_redirects(
     mock_set_up_bucket_on_aws, client):

    mock_set_up_bucket_on_aws.return_value = (False, 'Some error happened')

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    data = {
        'access-key-id': 'test',
        'secret-access-key': 'test',
        'bucket-name': 'test'
    }
    response = client.post(
        '/s3/settings/add_bucket', data=data)

    assert response.status_code == 302
    assert response.location == 'http://localhost/s3/settings'


@mock.patch('goodtablesio.integrations.s3.blueprint.disable_bucket_on_aws')
def test_s3_settings_remove_bucket_success(mock_disable_bucket_on_aws, client):

    bucket = factories.S3Bucket(
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})

    mock_disable_bucket_on_aws.return_value = (True, '')

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get(
        '/s3/settings/remove_bucket/{}'.format(bucket.name),
        follow_redirects=True)

    # TODO: improve when final UI is in place
    # body = response.get_data(as_text=True)
    # assert 'Bucket removed' in body, body

    buckets = database['session'].query(S3Bucket).all()

    assert buckets[0].name == bucket.name
    assert buckets[0].active is False


@mock.patch('goodtablesio.integrations.s3.blueprint.disable_bucket_on_aws')
def test_s3_settings_remove_bucket_failure(mock_disable_bucket_on_aws, client):

    bucket = factories.S3Bucket(
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})

    mock_disable_bucket_on_aws.return_value = (False, 'Some error happened')

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get(
        '/s3/settings/remove_bucket/{}'.format(bucket.name),
        follow_redirects=True)

    # TODO: improve when final UI is in place
    # body = response.get_data(as_text=True)
    # assert 'Some error happened' in body, body


def test_s3_settings_remove_bucket_not_found(client):

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get(
        '/s3/settings/remove_bucket/not_found',
        follow_redirects=True)

    # TODO: improve when final UI is in place
    # body = response.get_data(as_text=True)
    # assert 'Unknown bucket' in body, body


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
