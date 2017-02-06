import logging

from goodtablesio.services import database
from goodtablesio.integrations.s3.models.bucket import S3Bucket
from goodtablesio.integrations.s3.utils.s3client import S3Client
from goodtablesio.integrations.s3.utils.lambdaclient import LambdaClient
from goodtablesio.integrations.s3.exceptions import S3Exception


log = logging.getLogger(__name__)


def set_up_bucket_on_aws(access_key_id, secret_access_key, bucket_name):

    # Init clients
    lambda_client = LambdaClient()
    s3_client = S3Client(access_key_id, secret_access_key)

    try:
        # Check connections
        _check_connection(lambda_client, s3_client, bucket_name)

        # Add bucket policy
        _add_policy(lambda_client, s3_client, bucket_name)

        # Add lambda_permission
        _add_lambda_permission(lambda_client, s3_client, bucket_name)

        # Add notification
        _add_notification(lambda_client, s3_client, bucket_name)
    except S3Exception as e:
        message = str(e)
        if e.code == 's3-access-denied' and e.operation:
            message += ' ({})'.format(e.operation)
        return False, message

    return True, ''


def create_bucket(bucket_name, active=True, user=None):

    bucket = S3Bucket(name=bucket_name, active=active)
    if user:
        bucket.users.append(user)
    database['session'].add(bucket)
    database['session'].commit()

    return bucket


def _check_connection(lambda_client, s3_client, bucket_name):
    try:
        lambda_client.check_connection()
        s3_client.check_connection(bucket_name)
    except S3Exception as e:
        log.exception(e)
        raise e


def _add_policy(lambda_client, s3_client, bucket_name):
    try:
        s3_client.add_policy_for_lambda(bucket_name)
    except S3Exception as e:
        log.exception(e)
        raise e


def _add_lambda_permission(lambda_client, s3_client, bucket_name):
    try:
        lambda_client.add_permission_to_bucket(bucket_name)
    except S3Exception as e:
        # Revert changes
        try:
            s3_client.remove_policy_for_lambda(bucket_name)
        except S3Exception as sub_e:
            log.error('Additional error when removing policy from bucket')
            log.exception(sub_e)

        raise e


def _add_notification(lambda_client, s3_client, bucket_name):
    try:
        s3_client.add_notification(bucket_name)
    except S3Exception as e:
        # Revert changes
        try:
            lambda_client.remove_permission_to_bucket(bucket_name)
        except S3Exception as sub_e:
            log.error('Additional error when removing permission from lambda')
            log.exception(sub_e)

        try:
            s3_client.remove_policy_for_lambda(bucket_name)
        except S3Exception as sub_e:
            log.error('Additional error when removing policy from bucket')
            log.exception(sub_e)

        raise e
