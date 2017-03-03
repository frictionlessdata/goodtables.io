import logging

import boto3
import botocore

from goodtablesio import models
from goodtablesio.services import database
from goodtablesio.celery_app import celery_app
from goodtablesio.utils.jobtask import JobTask
from goodtablesio.utils.jobconf import make_validation_conf


log = logging.getLogger(__name__)


@celery_app.task(name='goodtablesio.s3.get_validation_conf', base=JobTask)
def get_validation_conf(bucket, job_id):

    job = database['session'].query(models.job.Job).get(job_id)

    if not job:
        return None

    # Update job
    models.job.update({
        'id': job_id,
        'status': 'running'
    })

    access_key_id = job.source.access_key_id
    secret_access_key = job.source.secret_access_key
    bucket_name = job.source.name

    client = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key)

    # Get job conf text (if it exists)
    try:
        yml_file = client.get_object(Bucket=bucket_name, Key='goodtables.yml')
        job_conf_text = yml_file['Body'].read()
    except botocore.exceptions.ClientError as exception:
        job_conf_text = None

    # Get all keys and create validation conf

    # TODO: can we filter at this point
    objects = client.list_objects(Bucket=bucket_name)

    # Get job files
    job_files = [o['Key'] for o in objects['Contents']]

    validation_conf = make_validation_conf(job_conf_text, job_files)

    # Create a tmp link for each file
    for _item in validation_conf['source']:

        _item['source'] = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': _item['source']},
            ExpiresIn=600)

    return validation_conf
