import json
import logging

import boto3
import botocore

from goodtablesio import settings
from goodtablesio.integrations.s3.exceptions import S3Exception


log = logging.getLogger(__name__)


class LambdaClient(object):

    def __init__(self):
        """
        Initialize a client for AWS Lambda authenticated against the main
        goodtables account.

        This is the account that hosts the notifications Lamda function.
        It uses the credentials stored as env vars.
        """

        self.lambda_arn = settings.S3_LAMBDA_ARN

        self.client = boto3.client(
            'lambda',
            region_name=settings.S3_GT_AWS_REGION,
            aws_access_key_id=settings.S3_GT_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_GT_SECRET_ACCESS_KEY)

    def _statement_id_for_bucket(self, bucket_name):
        return 'gt_lambda_bucket_perm_{}'.format(bucket_name)

    def _arn_for_bucket(self, bucket_name):
        return 'arn:aws:s3:::{}'.format(bucket_name)

    def check_connection(self):
        try:
            return self.client.get_function(FunctionName=self.lambda_arn)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'EndpointConnectionError':
                raise S3Exception(
                    'Could not connect to the Lambda endpoint: {}'.format(e),
                    's3-connection-error')
            elif e.response['Error']['Code'] == 'InvalidAccessKeyId':
                raise S3Exception(
                    'Invalid Access Key', 's3-invalid-access-key')
            elif e.response['Error']['Code'] == 'SignatureDoesNotMatch':
                raise S3Exception(
                    'Invalid signature, please check your secret key',
                    's3-invalid-signature')
            elif e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception(
                    'AWS Lambda function not found: {}'.format(e),
                    's3-lambda-not-found')
            elif e.response['Error']['Code'] == 'AccessDeniedException':
                raise S3Exception(
                    'Access denied', 's3-access-denied', 'get-function')
            raise e

    def get_buckets_with_permissions(self):

        policy = self.client.get_policy(FunctionName=self.lambda_arn)

        policy = json.loads(policy['Policy'])

        buckets = []
        for statement in policy['Statement']:
            if (statement['Action'] == 'lambda:InvokeFunction' and
                    statement['Effect'] == 'Allow' and
                    statement['Condition']):

                bucket_arn = statement['Condition']['ArnLike']['AWS:SourceArn']
                buckets.append(bucket_arn.replace('arn:aws:s3:::', ''))

        return buckets

    def add_permission_to_bucket(self, bucket_name):

        statement_id = self._statement_id_for_bucket(bucket_name)

        try:
            self.client.add_permission(
                FunctionName=self.lambda_arn,
                StatementId=statement_id,
                Action='lambda:InvokeFunction',
                Principal='s3.amazonaws.com',
                SourceArn=self._arn_for_bucket(bucket_name))

            log.debug('Added permission to bucket {0} on lambda'.format(
                bucket_name))

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceConflictException':
                raise S3Exception(
                    'Bucket alredy has permission on function: {}'.format(
                        bucket_name), 's3-bucket-has-already-perm-on-lambda')
            raise e

    def remove_permission_to_bucket(self, bucket_name):

        statement_id = self._statement_id_for_bucket(bucket_name)

        try:
            self.client.remove_permission(
                FunctionName=self.lambda_arn,
                StatementId=statement_id)

            log.debug('Removed permission for bucket {0} on lambda'.format(
                bucket_name))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception('Permission not found : {0}'.format(
                    statement_id), 's3-lambda-perm-not-found')
            raise e
