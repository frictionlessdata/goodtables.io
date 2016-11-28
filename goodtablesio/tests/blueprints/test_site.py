import pytest

from goodtablesio import helpers

# Clean up DB on all this module's tests

pytestmark = pytest.mark.usefixtures('db_cleanup')


def test_site_basic(client):

    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

    # TODO: Test actual content when implemented


def test_site_get_job(client):

    helpers.insert_job_row('101')

    response = client.get('/job/101')

    # TODO: Test actual content when implemented

    body = response.get_data(as_text=True)
    assert 'Report' in body
    assert '101' in body


def test_site_get_job_not_found(client):

    response = client.get('/job/xxx')

    assert response.status_code == 404
