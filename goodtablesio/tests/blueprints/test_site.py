import datetime

import pytest

from goodtablesio.tests import factories


# Clean up DB on all this module's tests

pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_site_home_not_logged_in(client):

    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

    # TODO: Test actual content when implemented

    body = response.get_data(as_text=True)
    assert "const component = 'Home'" in body


def test_site_home_logged_in(client):

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get('/')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost:5000/dashboard'


def test_site_dashboard_not_logged_in(client):

    response = client.get('/dashboard')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost:5000/'


def test_site_dashboard_logged_in(client):

    user = factories.User()

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = user.id

    response = client.get('/dashboard')

    assert response.status_code == 200

    # TODO: Test actual content when implemented

    body = response.get_data(as_text=True)
    assert 'Dashboard' in body


def test_site_get_job(client):

    job = factories.Job()

    response = client.get('/jobs/{0}'.format(job.id))

    # TODO: Test actual content when implemented

    body = response.get_data(as_text=True)
    assert 'html' in body


def test_site_get_job_not_found(client):

    response = client.get('/jobs/xxx')

    assert response.status_code == 404


def test_site_get_jobs(client):
    job = factories.Job()
    response = client.get('/jobs')
    body = response.get_data(as_text=True)
    assert 'Jobs' in body
    assert job.id in body


def test_badge_not_found(client):

    response = client.get('/badge/s3/not-found.svg')

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()


def test_badge_source_exists_but_no_jobs(client):

    bucket = factories.S3Bucket()

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()


def test_badge_source_exists_job_created(client):

    bucket = factories.S3Bucket()
    factories.Job(source=bucket, integration_name='s3', status='created')

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()


def test_badge_source_exists_job_running(client):

    bucket = factories.S3Bucket()
    factories.Job(source=bucket, integration_name='s3', status='running')

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()


def test_badge_source_exists_job_error(client):

    bucket = factories.S3Bucket()
    factories.Job(source=bucket, integration_name='s3', status='error')

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>error</text></g>' in response.get_data()


def test_badge_source_exists_job_success(client):

    bucket = factories.S3Bucket()
    factories.Job(source=bucket, integration_name='s3', status='success')

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>valid</text></g>' in response.get_data()


def test_badge_source_exists_job_failure(client):

    bucket = factories.S3Bucket()
    factories.Job(source=bucket, integration_name='s3', status='failure')

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>invalid</text></g>' in response.get_data()


def test_badge_source_exists_picks_last_finished_job(client):

    bucket = factories.S3Bucket()
    factories.Job(source=bucket, integration_name='s3', status='success',
                  finished=datetime.datetime.utcnow())
    factories.Job(source=bucket, integration_name='s3', status='failure',
                  finished=datetime.datetime.utcnow())
    factories.Job(source=bucket, integration_name='s3', status='running')

    response = client.get('/badge/s3/{}.svg'.format(bucket.name))

    assert response.content_type == 'image/svg+xml'
    assert b'>invalid</text></g>' in response.get_data()


def test_badge_works_on_github_repos(client):

    repo = factories.GithubRepo()
    factories.Job(source=repo, integration_name='github', status='success')

    response = client.get('/badge/github/{}/{}.svg'.format(repo.owner,
                                                           repo.repo))

    assert response.content_type == 'image/svg+xml'
    assert b'>valid</text></g>' in response.get_data()


def test_badge_source_defaults_to_flat(client):

    response = client.get('/badge/s3/not_found.svg')

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()
    assert b'<linearGradient' in response.get_data()


def test_badge_source_wrong_style_defaults_to_flat(client):

    response = client.get('/badge/s3/not_found.svg?style=not-found')

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()
    assert b'<linearGradient' in response.get_data()


def test_badge_source_supports_flat_square(client):

    response = client.get('/badge/s3/not_found.svg?style=flat-square')

    assert response.content_type == 'image/svg+xml'
    assert b'>unknown</text></g>' in response.get_data()
    assert b'<linearGradient' not in response.get_data()
