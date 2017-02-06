from goodtablesio.models.source import Source


class S3Bucket(Source):

    __mapper_args__ = {
        'polymorphic_identity': 's3'
    }
