import pytest
import botocore
from botocore.stub import Stubber

from goodtablesio import settings
from goodtablesio.plugins.s3.utils import LambdaClient, S3Client
from goodtablesio.plugins.s3.exceptions import S3Exception
from goodtablesio.tests.plugins.s3 import mock_responses


def test_s3_client_init():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    assert hasattr(client.client, 'list_buckets')


def test_s3_client_notification_id_for_bucket():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    assert (client._notification_id_for_bucket('test') ==
            'goodtablesio_notification_test')


def test_s3_client_statement_id_for_bucket():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    assert (client._statement_id_for_bucket('test') ==
            'goodtablesio_policy_statement_test')


def test_s3_client_add_notification():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'put_bucket_notification_configuration',
            mock_responses.s3_put_bucket_notification_configuration)

        client.add_notification('test-gtio-2')


def test_s3_client_add_notification_bucket_not_found():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'put_bucket_notification_configuration',
            'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.add_notification('test-not-found')

            assert 'Bucket not found' in str(exc)


def test_s3_client_add_notification_access_denied():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'put_bucket_notification_configuration',
            'AccessDenied')

        with pytest.raises(S3Exception) as exc:
            client.add_notification('test-gtio-2')

            assert 'Access denied' in str(exc)


def test_s3_client_add_notification_no_perms_on_lamda():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'put_bucket_notification_configuration',
            'InvalidArgument')

        with pytest.raises(S3Exception) as exc:
            client.add_notification('test-gtio-2')

            assert 'Bucket does not have permission on lambda' in str(exc)


def test_s3_client_add_notification_other_exception():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'put_bucket_notification_configuration',
            'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.add_notification('test-gtio-2')


def test_s3_client_remove_notification():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_notification_configuration',
            mock_responses.s3_get_bucket_notification_configuration)

        stubber.add_response(
            'put_bucket_notification_configuration',
            mock_responses.s3_put_bucket_notification_configuration)

        client.remove_notification('test-gtio-2')


def test_s3_client_remove_notification_bucket_not_found():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_notification_configuration',
            'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.remove_notification('test-not-found')

            assert 'Bucket not found' in str(exc)


def test_s3_client_remove_notification_access_denied_get():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_notification_configuration',
            'AccessDenied')

        with pytest.raises(S3Exception) as exc:
            client.remove_notification('test-gtio-2')

            assert 'Access denied (get notification)' in str(exc)


def test_s3_client_remove_notification_other_exception_get():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_notification_configuration',
            'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.remove_notification('test-gtio-2')


def test_s3_client_remove_notification_access_denied_put():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_notification_configuration',
            mock_responses.s3_get_bucket_notification_configuration)

        stubber.add_client_error(
            'put_bucket_notification_configuration',
            'AccessDenied')

        with pytest.raises(S3Exception) as exc:
            client.remove_notification('test-gtio-2')

            assert 'Access denied (put notification)' in str(exc)


def test_s3_client_remove_notification_other_exception_put():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_notification_configuration',
            mock_responses.s3_get_bucket_notification_configuration)

        stubber.add_client_error(
            'put_bucket_notification_configuration',
            'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.remove_notification('test-gtio-2')


def test_s3_remove_notification_conf_lambda_present():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    conf = {
        'LambdaFunctionConfigurations': [
            {
                'Events': ['s3:ObjectCreated:*'],
                'Id': 'goodtablesio_notification_test-gtio-1',
                'LambdaFunctionArn': 'someArn'
            }
        ],
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    expected_conf = {
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    new_conf = client._update_conf_to_remove_lambda_notification(
        conf, 'test-gtio-1')
    assert new_conf == expected_conf


def test_s3_remove_notification_conf_lambda_present_other_id_and_other():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    conf = {
        'LambdaFunctionConfigurations': [
            {
                'Events': ['s3:ObjectCreated:*'],
                'Id': 'goodtablesio_notification_test-gtio-1',
                'LambdaFunctionArn': 'someArn'
            },
            {
                'Events': ['s3:ObjectCreated:*'],
                'Id': 'other-id',
                'LambdaFunctionArn': 'otherArn'
            }

        ],
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    expected_conf = {
        'LambdaFunctionConfigurations': [
            {
                'Events': ['s3:ObjectCreated:*'],
                'Id': 'other-id',
                'LambdaFunctionArn': 'otherArn'
            }

        ],
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    new_conf = client._update_conf_to_remove_lambda_notification(
        conf, 'test-gtio-1')
    assert new_conf == expected_conf


def test_s3_remove_notification_conf_lambda_present_other_id():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    conf = {
        'LambdaFunctionConfigurations': [
            {
                'Events': ['s3:ObjectCreated:*'],
                'Id': 'goodtablesio_notification_test-gtio-2',
                'LambdaFunctionArn': settings.S3_LAMBDA_ARN
            }
        ],
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    expected_conf = conf

    new_conf = client._update_conf_to_remove_lambda_notification(
        conf, 'test-gtio-1')
    assert new_conf == expected_conf


def test_s3_remove_notification_conf_lambda_empty_other():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    conf = {
        'LambdaFunctionConfigurations': [],
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    expected_conf = {
        'TopicConfigurations': [{'a': 'b'}],
        'QueueConfigurations': [{'a': 'b'}],
    }

    new_conf = client._update_conf_to_remove_lambda_notification(
        conf, 'test-gtio-1')
    assert new_conf == expected_conf


def test_s3_remove_notification_conf_lambda_empty():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    conf = {
        'LambdaFunctionConfigurations': []
    }

    expected_conf = None

    new_conf = client._update_conf_to_remove_lambda_notification(
        conf, 'test-gtio-1')
    assert new_conf == expected_conf


def test_s3_remove_notification_conf_lambda_empty_dict():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    conf = {
    }

    expected_conf = None

    new_conf = client._update_conf_to_remove_lambda_notification(
        conf, 'test-gtio-1')
    assert new_conf == expected_conf


def test_s3_client_get_bucket_policy():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        policy = client.get_bucket_policy('test-gtio-1')

        assert policy == mock_responses.policy


def test_s3_client_get_bucket_policy_no_policy():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_policy',
            'NoSuchBucketPolicy')

        policy = client.get_bucket_policy('test-gtio-1')

        assert policy is None


def test_s3_client_get_bucket_policy_bucket_not_found():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_policy',
            'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.get_bucket_policy('test-not-found')

            assert 'Bucket not found' in str(exc)


def test_s3_client_get_bucket_policy_access_denied():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_policy',
            'AccessDenied')

        with pytest.raises(S3Exception) as exc:
            client.get_bucket_policy('test-gtio-1')

            assert 'Access denied' in str(exc)


def test_s3_client_get_bucket_policy_other_error():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_client_error(
            'get_bucket_policy',
            'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.get_bucket_policy('test-gtio-1')


def test_s3_update_policy_to_add_statement_no_existing_policy():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    policy = None

    expected_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'goodtablesio_policy_statement_test-gtio-1',
                'Effect': 'Allow',
                'Principal': {
                    'AWS': settings.S3_GT_ACCOUNT_ID
                },
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            }
        ]
    }

    new_policy = client._update_policy_to_add_statement(policy, 'test-gtio-1')
    assert new_policy == expected_policy


def test_s3_update_policy_to_add_statement_existing_policy():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'goodtablesio_policy_statement_test-gtio-1',
                'Effect': 'Allow',
                'Principal': {
                    'AWS': settings.S3_GT_ACCOUNT_ID
                },
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            }
        ]
    }

    expected_policy = None

    new_policy = client._update_policy_to_add_statement(policy, 'test-gtio-1')
    assert new_policy == expected_policy


def test_s3_update_policy_to_add_statement_existing_other_policy():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'some_other_policy',
                'Effect': 'Allow',
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            }
        ]
    }

    expected_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'goodtablesio_policy_statement_test-gtio-1',
                'Effect': 'Allow',
                'Principal': {
                    'AWS': settings.S3_GT_ACCOUNT_ID
                },
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            },
            {
                'Sid': 'some_other_policy',
                'Effect': 'Allow',
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            }
        ]
    }

    new_policy = client._update_policy_to_add_statement(policy, 'test-gtio-1')

    new_policy['Statement'] = sorted(
        new_policy['Statement'], key=lambda k: k['Sid'])
    assert new_policy == expected_policy


def test_s3_client_add_bucket_policy():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_response(
            'put_bucket_policy',
            mock_responses.s3_put_bucket_policy)

        client.add_policy_for_lambda('test-gtio-2')


def test_s3_client_add_bucket_policy_already_exists():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        assert client.add_policy_for_lambda('test-gtio-1') is None


def test_s3_client_add_policy_bucket_not_found():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_client_error(
            'put_bucket_policy',
            'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.add_policy_for_lambda('test-not-found')

            assert 'Bucket not found' in str(exc)


def test_s3_client_add_policy_access_denied():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_client_error(
            'put_bucket_policy',
            'AccessDenied')

        with pytest.raises(S3Exception) as exc:
            client.add_policy_for_lambda('test-gtio-2')

            assert 'Access denied' in str(exc)


def test_s3_client_add_policy_other_exception():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_client_error(
            'put_bucket_policy',
            'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.add_policy_for_lambda('test-gtio-2')


def test_s3_update_policy_to_remove_statement_existing():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'goodtablesio_policy_statement_test-gtio-1',
                'Effect': 'Allow',
                'Principal': {
                    'AWS': settings.S3_GT_ACCOUNT_ID
                },
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            },
            {
                'Sid': 'some_other_policy',
                'Effect': 'Allow',
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            }
        ]
    }

    expected_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'some_other_policy',
                'Effect': 'Allow',
                'Action': [
                    's3:ListBucket',
                    's3:GetBucketLocation',
                    's3:GetBucketNotification'
                ],
                'Resource': 'arn:aws:s3:::test-gtio-1'
            }
        ]
    }

    new_policy = client._update_policy_to_remove_statement(
        policy, 'test-gtio-1')

    assert new_policy == expected_policy


def test_s3_client_remove_policy_bucket_statement_statement_only_one():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_response(
            'delete_bucket_policy',
            mock_responses.s3_delete_bucket_policy)

        client.remove_policy_for_lambda('test-gtio-1')


def test_s3_client_remove_policy_bucket_statement_statement_many():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy_many_statements)

        stubber.add_response(
            'put_bucket_policy',
            mock_responses.s3_put_bucket_policy)

        client.remove_policy_for_lambda('test-gtio-1')


def test_s3_client_remove_policy_bucket_policy_does_not_exist():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:

        stubber.add_client_error(
            'get_bucket_policy',
            'NoSuchBucketPolicy')

        assert client.remove_policy_for_lambda('test-gtio-2') is None


def test_s3_client_remove_policy_bucket_statement_does_not_exist():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        assert client.remove_policy_for_lambda('test-gtio-2') is None


def test_s3_client_remove_policy_bucket_not_found():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_client_error(
            'delete_bucket_policy',
            'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.remove_policy_for_lambda('test-gtio-1')

            assert 'Bucket not found' in str(exc)


def test_s3_client_remove_policy_access_denied():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_client_error(
            'delete_bucket_policy',
            'AccessDenied')

        with pytest.raises(S3Exception) as exc:
            client.remove_policy_for_lambda('test-gtio-1')

            assert 'Access denied' in str(exc)


def test_s3_client_remove_policy_other_exception():

    client = S3Client('mock_access_key_id', 'mock_secret_access_key')

    with Stubber(client.client) as stubber:
        stubber.add_response(
            'get_bucket_policy',
            mock_responses.s3_get_bucket_policy)

        stubber.add_client_error(
            'delete_bucket_policy',
            'EndpointConnectionError')

        with pytest.raises(botocore.exceptions.ClientError):
            client.remove_policy_for_lambda('test-gtio-1')


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


def test_lambda_client_check_connection_wrong_arn():

    client = LambdaClient()

    with Stubber(client.client) as stubber:
        stubber.add_client_error('get_function', 'ResourceNotFound')

        with pytest.raises(S3Exception) as exc:
            client.check_connection()

            assert 'Lambda function not found' in str(exc)


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
