import pytest
import botocore
from botocore.stub import Stubber

from goodtablesio import settings
from goodtablesio.plugins.s3.utils import LambdaClient
from goodtablesio.plugins.s3.exceptions import S3Exception
from goodtablesio.tests.plugins.s3 import mock_responses


def test_lambda_client_init():

    client = LambdaClient()

    assert hasattr(client.client, 'get_function')
    assert client.client.meta.region_name == settings.S3_GT_AWS_REGION


def test_lambda_client_check_connection():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_function',
            mock_responses.lambda_get_function)

        function_info = client.check_connection()

    assert (function_info['Configuration']['FunctionArn'] ==
            settings.S3_LAMBDA_ARN)


def test_lambda_client_check_connection_error():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function', 'EndpointConnectionError')

        with pytest.raises(S3Exception) as exc:
            client.check_connection()

            assert 'Could not connect' in str(exc)


def test_lambda_client_check_connection_invalid_key():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function', 'InvalidAccessKeyId')

        with pytest.raises(S3Exception) as exc:
            client.check_connection()

            assert 'Invalid Access Key' in str(exc)


def test_lambda_client_check_connection_invalid_signature():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function', 'SignatureDoesNotMatch')

        with pytest.raises(S3Exception) as exc:
            client.check_connection()

            assert 'Invalid signature' in str(exc)


def test_lambda_client_check_connection_wrong_arn():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function', 'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.check_connection()

            assert 'Lambda function not found' in str(exc)


def test_lambda_client_check_connection_access_denied():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function', 'AccessDeniedException')

        with pytest.raises(S3Exception) as exc:
            client.check_connection()

            assert 'Access denied' in str(exc)


def test_lambda_client_check_connection_other_error():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function')

        with pytest.raises(botocore.exceptions.ClientError):
            client.check_connection()


def test_lambda_client_arn_for_bucket():

    client = LambdaClient()

    assert client._arn_for_bucket('test') == 'arn:aws:s3:::test'


def test_lambda_client_get_buckets_with_permissions():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_response('get_policy', mock_responses.lambda_get_policy)

        buckets = client.get_buckets_with_permissions()

    assert buckets == ['test-goodtables', 'test-gtio-1']


def test_lambda_client_add_permission_to_bucket():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'add_permission', mock_responses.lambda_add_permission)

        client.add_permission_to_bucket('test-gtio-2')


def test_lambda_client_add_permission_to_bucket_already_exists():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('add_permission', 'ResourceConflictException')

        with pytest.raises(S3Exception) as exc:
            client.add_permission_to_bucket('test-gtio-2')

            assert 'Bucket already has permission' in str(exc)


def test_lambda_client_add_permission_to_bucket_other_exception():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('add_permission', 'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.add_permission_to_bucket('test-gtio-2')


def test_lambda_client_remove_permission_to_bucket():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_response('remove_permission',
                             mock_responses.lambda_remove_permission)

        client.remove_permission_to_bucket('test-gtio-2')


def test_lambda_client_remove_permission_to_bucket_doesnt_exist():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('remove_permission', 'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.remove_permission_to_bucket('test-gtio-2')

            assert 'Permission not found' in str(exc)


def test_lambda_client_remove_permission_to_bucket_other_exception():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('remove_permission',
                                 'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.remove_permission_to_bucket('test-gtio-2')
