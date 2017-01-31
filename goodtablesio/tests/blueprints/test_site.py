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
    assert 'Welcome' in body


def test_site_home_logged_in(client):

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = 'xxx'

    response = client.get('/')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/dashboard'


def test_site_dashboard_not_logged_in(client):

    response = client.get('/dashboard')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'


def test_site_dashboard_logged_in(client):

    with client.session_transaction() as sess:
        # Mock a user login
        sess['user_id'] = 'xxx'

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
