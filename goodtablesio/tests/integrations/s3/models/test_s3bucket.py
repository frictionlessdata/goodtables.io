import pytest
from goodtablesio.tests import factories
from goodtablesio.services import database
from goodtablesio.models.user import User
from goodtablesio.integrations.github.models.repo import GithubRepo
from goodtablesio.integrations.s3.models.bucket import S3Bucket

pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

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


# https://github.com/frictionlessdata/goodtables.io/issues/192
def test_delete_bucket():
    user = factories.User()
    repo = factories.GithubRepo(users=[user], active=True)
    bucket = factories.S3Bucket(users=[user], active=True)
    repo = database['session'].query(GithubRepo).one()
    bucket = database['session'].query(S3Bucket).one()
    database['session'].delete(bucket)
    database['session'].commit()
    users = database['session'].query(User).all()
    repos = database['session'].query(GithubRepo).all()
    buckets = database['session'].query(S3Bucket).all()
    assert len(users) == 1
    assert len(repos) == 1
    assert len(buckets) == 0
