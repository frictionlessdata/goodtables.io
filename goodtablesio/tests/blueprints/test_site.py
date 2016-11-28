import pytest

from goodtablesio.tests import factories


# Clean up DB on all this module's tests

pytestmark = pytest.mark.usefixtures('db_cleanup')


def test_site_basic(client):

    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

    # TODO: Test actual content when implemented


def test_site_get_job(client):

    job = factories.Job()

    response = client.get('/job/{0}'.format(job.job_id))

    # TODO: Test actual content when implemented

    body = response.get_data(as_text=True)
    assert 'Report' in body
    assert job.job_id in body


def test_site_get_job_not_found(client):

    response = client.get('/job/xxx')

    assert response.status_code == 404
