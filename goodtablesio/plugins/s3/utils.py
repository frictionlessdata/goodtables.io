import json
import logging

import boto3
import botocore

from goodtablesio import settings, exceptions


log = logging.getLogger(__name__)


class S3Exception(exceptions.GoodtablesioException):
    pass


# TODO: check connection :invalid access key

class S3Client(object):

    def __init__(self, access_key_id, secret_access_key):
        """
        Initializes a client for a user provided S3 bucket

        Arguments:
            access_key_id (str): The Access Key Id part of the credentials
            secret_access_key (str): The Secret Access Key part of the
                credentials

        """
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

    def _notification_id_for_bucket(self, bucket_name):
        return 'goodtablesio_notification_{}'.format(bucket_name)

    def _statement_id_for_bucket(self, bucket_name):
        return 'goodtablesio_policy_statement_{}'.format(bucket_name)

    def add_notification(self, bucket_name):

        conf = {
            'LambdaFunctionConfigurations': [
                {
                    'Id': self._notification_id_for_bucket(bucket_name),
                    'LambdaFunctionArn': settings.S3_LAMBDA_ARN,
                    'Events': [
                        's3:ObjectCreated:*'
                    ]
                },
            ]
        }

        try:
            self.client.put_bucket_notification_configuration(
                Bucket=bucket_name,
                NotificationConfiguration=conf)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception('Bucket not found: {0}'.format(
                    bucket_name))
            elif e.response['Error']['Code'] == 'AccessDenied':
                raise S3Exception(
                    'Access denied (add notification): {0}'.format(
                        bucket_name))
            elif e.response['Error']['Code'] == 'InvalidArgument':
                raise S3Exception('Bucket does not have permission on lambda '
                                  'function : {0}'.format(bucket_name))

            raise e

    def _update_conf_to_remove_lambda_notification(self, conf, bucket_name):

        conf.pop('ResponseMetadata', None)

        lambda_confs = conf.pop('LambdaFunctionConfigurations', None)

        if lambda_confs:
            new_lambda_confs = [
                c for c in lambda_confs
                if not c['Id'] == self._notification_id_for_bucket(
                    bucket_name)]

            if new_lambda_confs:
                conf['LambdaFunctionConfigurations'] = new_lambda_confs

        if conf == {}:
            conf = None

        return conf

    def remove_notification(self, bucket_name):

        try:
            conf = self.client.get_bucket_notification_configuration(
                Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception('Bucket not found : {0}'.format(
                    bucket_name))
            elif e.response['Error']['Code'] == 'AccessDenied':
                raise S3Exception(
                    'Access denied (get notification): {0}'.format(
                        bucket_name))
            raise e

        if conf:
            new_conf = self._update_conf_to_remove_lambda_notification(
                conf, bucket_name)

            try:
                self.client.put_bucket_notification_configuration(
                    Bucket=bucket_name,
                    NotificationConfiguration=new_conf)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied':
                    raise S3Exception(
                        'Access denied (remove notification): {0}'.format(
                            bucket_name))
                raise e

    def get_bucket_policy(self, bucket_name):
        try:
            policy = self.client.get_bucket_policy(
                Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                # Bucket has no policy
                return None
            elif e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception('Bucket not found : {0}'.format(
                    bucket_name))
            elif e.response['Error']['Code'] == 'AccessDenied':
                raise S3Exception(
                    'Access denied (get notification): {0}'.format(
                        bucket_name))
            raise e

        return json.loads(policy['Policy'])

    def _update_policy_to_add_statement(self, existing_policy, bucket_name):

        statement = {
            'Sid': self._statement_id_for_bucket(bucket_name),
            'Effect': 'Allow',
            'Principal': {
                'AWS': settings.S3_GT_ACCOUNT_ID
            },
            'Action': [
                's3:ListBucket',
                's3:GetBucketLocation',
                's3:GetBucketNotification'
            ],
            'Resource': 'arn:aws:s3:::{0}'.format(bucket_name)
        }

        if not existing_policy:
            new_policy = {
                'Version': '2012-10-17',
                'Statement': [statement]
            }
        else:

            exists = [
                s for s in existing_policy['Statement']
                if s['Sid'] == statement['Sid']]

            if exists:
                # Policy already applied to the bucket
                return None

            existing_policy['Statement'].append(statement)
            new_policy = existing_policy

        return new_policy

    def _update_policy_to_remove_statement(self, existing_policy, bucket_name):

        statement_id = self._statement_id_for_bucket(bucket_name)

        new_statements = [
            s for s in existing_policy['Statement']
            if s['Sid'] != statement_id]
        new_policy = existing_policy
        new_policy['Statement'] = new_statements

        return new_policy

    def add_policy_for_lambda(self, bucket_name):

        existing_policy = self.get_bucket_policy(bucket_name)

        new_policy = self._update_policy_to_add_statement(
            existing_policy, bucket_name)

        if not new_policy:
            return None

        try:
            self.client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(new_policy))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception('Bucket not found : {0}'.format(
                    bucket_name))
            elif e.response['Error']['Code'] == 'AccessDenied':
                raise S3Exception(
                    'Access denied (get notification): {0}'.format(
                        bucket_name))
            raise e

    def remove_policy_for_lambda(self, bucket_name):

        statement_id = self._statement_id_for_bucket(bucket_name)

        existing_policy = self.get_bucket_policy(bucket_name)

        if not existing_policy:
            return None

        exists = [
            s for s in existing_policy['Statement']
            if s['Sid'] == statement_id]

        if not exists:
            # Policy not present in the bucket
            return
        try:
            if len(existing_policy['Statement']) == 1:
                self.client.delete_bucket_policy(Bucket=bucket_name)
            else:

                new_policy = self._update_policy_to_remove_statement(
                    existing_policy, bucket_name)

                self.client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=json.dumps(new_policy))

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception('Bucket not found : {0}'.format(
                    bucket_name))
            elif e.response['Error']['Code'] == 'AccessDenied':
                raise S3Exception(
                    'Access denied (get notification): {0}'.format(
                        bucket_name))
            raise e


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
                    'Could not connect to the Lambda endpoint: {}'.format(e))
            elif e.response['Error']['Code'] == 'ResourceNotFound':
                raise S3Exception(
                    'AWS Lambda function not found: {}'.format(e))
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
                        bucket_name))
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
                    statement_id))
            raise e
