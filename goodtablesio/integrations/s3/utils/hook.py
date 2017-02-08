
def get_bucket_from_hook_payload(payload):

    try:
        bucket = payload['Records'][0]['s3']['bucket']['name']
    except (IndexError, KeyError, TypeError):
        bucket = None

    return bucket
