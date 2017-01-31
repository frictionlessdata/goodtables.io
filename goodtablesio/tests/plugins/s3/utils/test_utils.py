from unittest import mock

import pytest

from goodtablesio.plugins.s3.utils.s3client import S3Client
from goodtablesio.plugins.s3.utils.lambdaclient import LambdaClient
from goodtablesio.plugins.s3.utils import set_up_bucket
from goodtablesio.plugins.s3.exceptions import S3Exception


def test_set_up_bucket(mock_s3_client, mock_lambda_client):

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')
    assert set_up_bucket(*args) == (True, '')


def test_set_up_bucket_s3_connection_error(mock_lambda_client):

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')
    with mock.patch.object(S3Client, 'check_connection') as mock_call:
        mock_call.side_effect = S3Exception(
            'Could not connect to the S3 endpoint', 's3-connection-error')

        assert set_up_bucket(*args) == (
            False, 'Could not connect to the S3 endpoint')


def test_set_up_bucket_lambda_connection_error(mock_s3_client):

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')
    with mock.patch.object(LambdaClient, 'check_connection') as mock_call:
        mock_call.side_effect = S3Exception(
            'Could not connect to the Lambda endpoint', 's3-connection-error')

        assert set_up_bucket(*args) == (
            False, 'Could not connect to the Lambda endpoint')


def test_set_up_bucket_s3_add_policy_access_denied():

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')

    with mock.patch('goodtablesio.plugins.s3.utils._check_connection'), \
            mock.patch.object(S3Client, 'add_policy_for_lambda') as mock_call:

        mock_call.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'get-bucket-policy')

        assert set_up_bucket(*args) == (
            False, 'Access denied (get-bucket-policy)')


def test_set_up_bucket_lambda_add_permission_fails():

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')

    with mock.patch('goodtablesio.plugins.s3.utils._check_connection'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_policy'), \
            mock.patch.object(LambdaClient, 'add_permission_to_bucket') as a, \
            mock.patch.object(S3Client, 'remove_policy_for_lambda') as b:

        a.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'add-permission')

        assert set_up_bucket(*args) == (
            False, 'Access denied (add-permission)')

        b.assert_called_once_with('test_bucket')


def test_set_up_bucket_lambda_add_permission_fails_revert_also_fails():

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')

    with mock.patch('goodtablesio.plugins.s3.utils._check_connection'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_policy'), \
            mock.patch.object(LambdaClient, 'add_permission_to_bucket') as a, \
            mock.patch.object(S3Client, 'remove_policy_for_lambda') as b:

        a.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'add-permission')

        b.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'remove-policy')

        assert set_up_bucket(*args) == (
            False, 'Access denied (add-permission)')


def test_set_up_bucket_lambda_add_notification_fails():

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')

    with mock.patch('goodtablesio.plugins.s3.utils._check_connection'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_policy'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_lambda_permission'), \
            mock.patch.object(S3Client, 'add_notification') as a, \
            mock.patch.object(LambdaClient, 'remove_permission_to_bucket') as b, \
            mock.patch.object(S3Client, 'remove_policy_for_lambda') as c:

        a.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'add-notification')

        assert set_up_bucket(*args) == (
            False, 'Access denied (add-notification)')

        b.assert_called_once_with('test_bucket')

        c.assert_called_once_with('test_bucket')


def test_set_up_bucket_lambda_add_notification_fails_first_revert_also_fails():

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')

    with mock.patch('goodtablesio.plugins.s3.utils._check_connection'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_policy'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_lambda_permission'), \
            mock.patch.object(S3Client, 'add_notification') as a, \
            mock.patch.object(LambdaClient, 'remove_permission_to_bucket') as b, \
            mock.patch.object(S3Client, 'remove_policy_for_lambda') as c:

        a.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'add-notification')

        b.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'remove-permission')

        assert set_up_bucket(*args) == (
            False, 'Access denied (add-notification)')

        c.assert_called_once_with('test_bucket')


def test_set_up_bucket_lambda_add_notification_fails_second_revert_also_fails():

    args = ('mock_access_key_id', 'mock_secret_access_key', 'test_bucket')

    with mock.patch('goodtablesio.plugins.s3.utils._check_connection'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_policy'), \
            mock.patch('goodtablesio.plugins.s3.utils._add_lambda_permission'), \
            mock.patch.object(S3Client, 'add_notification') as a, \
            mock.patch.object(LambdaClient, 'remove_permission_to_bucket') as b, \
            mock.patch.object(S3Client, 'remove_policy_for_lambda') as c:

        a.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'add-notification')

        c.side_effect = S3Exception(
            'Access denied', 's3-access-denied', 'remove-permission')

        assert set_up_bucket(*args) == (
            False, 'Access denied (add-notification)')

        b.assert_called_once_with('test_bucket')


@pytest.fixture
def mock_lambda_client():
    mock_client = mock.patch('goodtablesio.plugins.s3.utils.LambdaClient')
    mock_client.start()
    yield mock_client
    mock_client.stop()


@pytest.fixture
def mock_s3_client():
    mock_client = mock.patch('goodtablesio.plugins.s3.utils.S3Client')
    mock_client.start()
    yield mock_client
    mock_client.stop()
