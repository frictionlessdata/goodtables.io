import pytest
from goodtablesio.tests import factories
from goodtablesio.services import database
from goodtablesio.integrations.s3.models.bucket import S3Bucket

pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_access_key_id_get():

    bucket = factories.S3Bucket(access_key_id='xxx')

    assert bucket.access_key_id == 'xxx'


def test_access_key_id_get_unencrypted():

    bucket = factories.S3Bucket(conf={'access_key_id': 'xxx'})

    assert bucket.access_key_id is None


def test_access_key_id_set():

    bucket = factories.S3Bucket()

    bucket.access_key_id = 'xxx'

    # Encrypted
    assert bucket.conf['access_key_id'].startswith('gAAA')

    database['session'].commit()
    bucket_db = database['session'].query(S3Bucket).first()

    assert bucket_db.access_key_id == 'xxx'


def test_access_key_id_del():

    bucket = factories.S3Bucket(access_key_id='xxx')

    del bucket.access_key_id

    assert bucket.access_key_id is None

    database['session'].commit()
    bucket_db = database['session'].query(S3Bucket).first()

    assert bucket_db.access_key_id is None


def test_secret_access_key_get():

    bucket = factories.S3Bucket(secret_access_key='xxx')

    assert bucket.secret_access_key == 'xxx'


def test_secret_access_key_get_unencrypted():

    bucket = factories.S3Bucket(conf={'secret_access_key': 'xxx'})

    assert bucket.secret_access_key is None


def test_secret_access_key_set():

    bucket = factories.S3Bucket()

    bucket.secret_access_key = 'xxx'

    # Encrypted
    assert bucket.conf['secret_access_key'].startswith('gAAA')

    database['session'].commit()
    bucket_db = database['session'].query(S3Bucket).first()

    assert bucket_db.secret_access_key == 'xxx'


def test_secret_access_key_del():

    bucket = factories.S3Bucket(secret_access_key='xxx')

    del bucket.secret_access_key

    assert bucket.secret_access_key is None

    database['session'].commit()
    bucket_db = database['session'].query(S3Bucket).first()

    assert bucket_db.secret_access_key is None
