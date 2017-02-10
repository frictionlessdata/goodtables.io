from unittest import mock

import pytest
import botocore

from goodtablesio.integrations.s3.tasks.jobconf import get_validation_conf
from goodtablesio.tests import factories
from goodtablesio.tests.integrations.s3 import mock_responses


pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_get_validation_conf():

    bucket = factories.S3Bucket(
        name='test=bucket',
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    job = factories.Job(source=bucket)

    def mock_make_api_call(self, operation_name, kwarg):
        if operation_name == 'GetObject':
            return mock_responses.s3_get_object
        elif operation_name == 'ListObjects':
            return mock_responses.s3_list_objects
        else:
            assert 0

    def mock_generate_presigned_url(*args, **kwargs):
        return 'https://example.com/presigned/{}'.format(
            kwargs['Params']['Key'])

    with mock.patch('botocore.client.BaseClient._make_api_call',
                    new=mock_make_api_call), \
            mock.patch('botocore.signers.generate_presigned_url',
                       new=mock_generate_presigned_url):

        expected = {
            'files': [
                {'source': 'https://example.com/presigned/councillors-address-3.csv'},
                {'source': 'https://example.com/presigned/councillors-address2.csv'}
            ],
            'settings': {'error_limit': 1}
        }

        assert get_validation_conf('test-gtio-1', job.id) == expected


def test_get_validation_conf_no_goodtables_yml():

    bucket = factories.S3Bucket(
        name='test=bucket',
        conf={'access_key_id': 'test', 'secret_access_key': 'test'})
    job = factories.Job(source=bucket)

    def mock_make_api_call(self, operation_name, kwarg):
        if operation_name == 'GetObject':
            response = {'Error': {'Code': 'NoSuchKey'}}
            raise botocore.exceptions.ClientError(response, 'GetObject')
        elif operation_name == 'ListObjects':
            return mock_responses.s3_list_objects
        else:
            assert 0

    def mock_generate_presigned_url(*args, **kwargs):
        return 'https://example.com/presigned/{}'.format(
            kwargs['Params']['Key'])

    with mock.patch('botocore.client.BaseClient._make_api_call',
                    new=mock_make_api_call), \
            mock.patch('botocore.signers.generate_presigned_url',
                       new=mock_generate_presigned_url):

        expected = {
            'files': [
                {'source': 'https://example.com/presigned/councillors-address-3.csv'},
                {'source': 'https://example.com/presigned/councillors-address2.csv'}
            ]
        }

        assert get_validation_conf('test-gtio-1', job.id) == expected


def test_get_validation_conf_no_job():

    assert get_validation_conf('test-gtio-1', 'not-found') is None
