import io
import datetime
import json

from goodtablesio import settings

# pylama:ignore=E501


def response_metadata(status=200):
    return {
        'HTTPHeaders': {
            'content-length': '0',
            'date': 'Tue, 24 Jan 2017 11:05:35 GMT',
            'server': 'AmazonS3',
            'x-amz-id-2': 'eCLnPXXXXXXXXXXXXXCcisaykBg+2UCoxz223qFGm5lWhkSfRBV1wzzjY=',
            'x-amz-request-id': 'XXXXXXXX030'},
        'HTTPStatusCode': status,
        'HostId': 'eCLnPGRrSDcHHXXXXXXXXXXXXX5lWhkSfRBV1wzzjY=',
        'RequestId': 'XXXXXXXXXX030',
        'RetryAttempts': 0
    }


s3_put_bucket_notification_configuration = {
    'ResponseMetadata': response_metadata()
}


s3_remove_bucket_notification_configuration = {
    'ResponseMetadata': response_metadata()
}


s3_get_bucket_notification_configuration = {
    'LambdaFunctionConfigurations': [
        {
            'Events': ['s3:ObjectCreated:*'],
            'Id': 'goodtablesio_notification_test-gtio-1',
            'LambdaFunctionArn': settings.S3_LAMBDA_ARN}
    ],
    'ResponseMetadata': response_metadata(200)
}


policy = {
    'Version': '2012-10-17',
    'Id': 'Policy1484220622722',
    'Statement': [
        {
            'Sid': 'goodtablesio_policy_statement_test-gtio-1',
            'Effect': 'Allow',
            'Principal': {'AWS': 'arn:aws:iam::XXXXXXX:root'},
            'Action': ['s3:ListBucket', 's3:GetBucketLocation', 's3:GetBucketNotification'],
            'Resource': 'arn:aws:s3:::test-gtio-1'
        }
    ]
}


policy_many_statements = {
    'Version': '2012-10-17',
    'Id': 'Policy1484220622722',
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
        },
        {
            'Sid': 'goodtablesio_policy_statement_test-gtio-1',
            'Effect': 'Allow',
            'Principal': {'AWS': 'arn:aws:iam::XXXXXXX:root'},
            'Action': ['s3:ListBucket', 's3:GetBucketLocation', 's3:GetBucketNotification'],
            'Resource': 'arn:aws:s3:::test-gtio-1'
        }
    ]
}


s3_get_bucket_location = {
    'LocationConstraint': 'us-west-2',
    'ResponseMetadata': response_metadata(200)
}


s3_get_bucket_policy = {
    'Policy': json.dumps(policy),
    'ResponseMetadata': response_metadata(200)
}


s3_get_bucket_policy_many_statements = {
    'Policy': json.dumps(policy_many_statements),
    'ResponseMetadata': response_metadata(200)
}


s3_put_bucket_policy = {
    'ResponseMetadata': response_metadata(203)
}


s3_delete_bucket_policy = {
    'ResponseMetadata': response_metadata(204)
}

goodtables_yml = '''
files: '*'
settings:
  error_limit: 1
'''

s3_get_object = {
    'AcceptRanges': 'bytes',
    'Body': io.StringIO(goodtables_yml),
    'ContentLength': 38,
    'ContentType': 'application/octet-stream',
    'ETag': '"af07230272ead6bef63ffc10f24fb685"',
    'LastModified': datetime.datetime(2017, 2, 7, 14, 30, 51),
    'Metadata': {},
    'ResponseMetadata': response_metadata(200)
}


s3_list_objects = {
    'Contents': [
        {
            'ETag': '"2391d7ddb6850eb8f77c4717c0600f84"',
            'Key': 'councillors-address-3.csv',
            'LastModified': datetime.datetime(2017, 1, 12, 10, 16, 8),
            'Owner': {
                'DisplayName': 'amercadero',
                 'ID': '3154f69d9784540a09efb2b938054fdb7caebfe442acdf038963bed0dffcfcd9'
            },
            'Size': 11232,
            'StorageClass': 'STANDARD'
        },
        {
            'ETag': '"2391d7ddb6850eb8f77c4717c0600f84"',
            'Key': 'councillors-address2.csv',
            'LastModified': datetime.datetime(2017, 2, 6, 16, 42, 10),
            'Owner': {
                'DisplayName': 'amercadero',
                'ID': '3154f69d9784540a09efb2b938054fdb7caebfe442acdf038963bed0dffcfcd9'
            },
            'Size': 11232,
            'StorageClass': 'STANDARD'
        },
        {
            'ETag': '"244a8c0a0926c411671d522f2a6adea8"',
            'Key': 'dmesg.png',
            'LastModified': datetime.datetime(2017, 2, 6, 16, 43, 4),
            'Owner': {
                'DisplayName': 'amercadero',
                'ID': '3154f69d9784540a09efb2b938054fdb7caebfe442acdf038963bed0dffcfcd9'
            },
            'Size': 127658,
            'StorageClass': 'STANDARD'
        },
        {
            'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
            'Key': 'my_data/',
            'LastModified': datetime.datetime(2017, 2, 7, 11, 11, 18),
            'Owner': {
                'DisplayName': 'amercadero',
                'ID': '3154f69d9784540a09efb2b938054fdb7caebfe442acdf038963bed0dffcfcd9'
            },
            'Size': 0,
            'StorageClass': 'STANDARD'
        }
    ],
    'EncodingType': 'url',
    'IsTruncated': False,
    'Marker': '',
    'MaxKeys': 1000,
    'Name': 'test-gtio-1',
    'Prefix': '',
    'ResponseMetadata': response_metadata(200)
}


lambda_get_function = {
    'Code': {
        'Location': 'https://awslambda-us-west-2-tasks.s3-us-west-2.amazonaws.com/snapshots/969878809488/notify-goodtablesio-XXXX5a07432?X-Amz-Security-Token=',
        'RepositoryType': 'S3'},
    'Configuration': {
        'CodeSha256': '5UkddOEL+cTXXXXXXXXXXXXXXXXX=',
        'CodeSize': 798,
        'Description': 'Test',
        'Environment': {
            'Variables': {
                'GOODTABLES_S3_HOOK_URL': 'http://example.com/s3/hook'}},
        'FunctionArn': settings.S3_LAMBDA_ARN,
        'FunctionName': 'notify-goodtablesio',
        'Handler': 'lambda_function.lambda_handler',
        'LastModified': '2017-01-11T15:30:11.449+0000',
        'MemorySize': 128,
        'Role': 'arn:aws:iam::9XXXX:role/service-role/lambda-goodtablesio',
        'Runtime': 'python2.7',
        'Timeout': 10,
        'Version': '$LATEST',
        'VpcConfig': {'SecurityGroupIds': [], 'SubnetIds': []}},
    'ResponseMetadata': response_metadata(200)
}


lambda_get_policy = {
    'Policy': '{"Version":"2012-10-17","Id":"default","Statement":[{"Sid":"lc-c6b01660-e884-440f-9191-dc006334cc7b","Effect":"Allow","Principal":{"Service":"s3.amazonaws.com"},"Action":"lambda:InvokeFunction","Resource":"{0}","Condition":{"ArnLike":{"AWS:SourceArn":"arn:aws:s3:::test-goodtables"}}},{"Sid":"gt_lambda_bucket_perm_test-gtio-1","Effect":"Allow","Principal":{"Service":"s3.amazonaws.com"},"Action":"lambda:InvokeFunction","Resource":"{0}","Condition":{"ArnLike":{"AWS:SourceArn":"arn:aws:s3:::test-gtio-1"}}}]}'.replace('{0}', settings.S3_LAMBDA_ARN),
    'ResponseMetadata': response_metadata(200)
}


lambda_add_permission = {
    'Statement': '{"Sid":"gt_lambda_bucket_perm_test-gtio-2","Resource":"{0}","Effect":"Allow","Principal":{"Service":"s3.amazonaws.com"},"Action":["lambda:InvokeFunction"],"Condition":{"ArnLike":{"AWS:SourceArn":"arn:aws:s3:::test-gtio-2"}}}'.replace('{0}', settings.S3_LAMBDA_ARN),
    'ResponseMetadata': response_metadata(201)
}


lambda_remove_permission = {
    'ResponseMetadata': response_metadata(204)
}


s3_notification_event = {
  'Records': [
    {
      'eventVersion': '2.0',
      'eventTime': '1970-01-01T00:00:00.000Z',
      'requestParameters': {
        'sourceIPAddress': '127.0.0.1'
      },
      's3': {
        'configurationId': 'testConfigRule',
        'object': {
          'eTag': '0123456789abcdef0123456789abcdef',
          'key': 'councillors-address.csv',
          'sequencer': '0A1B2C3D4E5F678901',
          'size': 1024
        },
        'bucket': {
          'ownerIdentity': {
            'principalId': 'EXAMPLE'
          },
          'name': 'test-gtio-1',
          'arn': 'arn:aws:s3:::test-gtio-1'
        },
        's3SchemaVersion': '1.0'
      },
      'responseElements': {
        'x-amz-id-2': 'EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH',
        'x-amz-request-id': 'EXAMPLE123456789'
      },
      'awsRegion': 'us-east-1',
      'eventName': 'ObjectCreated:Put',
      'userIdentity': {
        'principalId': 'EXAMPLE'
      },
      'eventSource': 'aws:s3'
    }
  ]
}
