import json
from unittest import mock

import pytest

from goodtablesio import models
from goodtablesio.tests import factories


# Clean up DB on all this module's tests

pytestmark = pytest.mark.usefixtures('session_cleanup')


# TODO reactivate tests once API auth is implemented

def _data(response):

    return json.loads(response.get_data(as_text=True))


@pytest.mark.xfail
def test_api_basic(client):

    response = client.get('/api/')

    assert response.status_code == 200
    assert response.content_type == 'application/json; charset=utf-8'


@pytest.mark.xfail
def test_api_job_list_empty(client):

    response = client.get('/api/job')

    assert _data(response) == []


@pytest.mark.xfail
def test_api_job_list(client):

    job1 = factories.Job()
    job2 = factories.Job()

    response = client.get('/api/job')

    assert _data(response) == [job2.id, job1.id]


@pytest.mark.xfail
def test_api_get_job(client):

    job = factories.Job()

    response = client.get('/api/job/{0}'.format(job.id))

    data = _data(response)

    # TODO: Update after #19

    assert 'report' in data
    assert data['id'] == job.id
    assert 'created' in data
    assert 'status' in data


@pytest.mark.xfail
def test_api_get_job_not_found(client):

    response = client.get('/api/job/xxx')

    assert response.status_code == 404

    assert _data(response) == {'message': 'Job not found'}


@pytest.mark.xfail
def test_api_create_job(client):

    payload = {'source': [{'source': 'http://example.com'}]}

    # NB: We can't post the payload directly in `data` as Werkzeug
    # will think that the `files` key are actual uploads

    with mock.patch('goodtablesio.tasks.validate'):
        response = client.post(
            '/api/job',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})

    assert response.status_code == 200

    job_id = response.get_data(as_text=True)
    assert models.job.get(job_id)


@pytest.mark.xfail
def test_api_create_job_empty_body(client):

    response = client.post('/api/job')

    assert response.status_code == 400

    assert _data(response) == {'message': 'Missing configuration'}


@pytest.mark.xfail
def test_api_create_job_wrong_params(client):

    payload = {'not_files': [{'source': 'http://example.com'}]}

    response = client.post(
        '/api/job',
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'})

    assert response.status_code == 400

    assert _data(response) == {'message': 'Invalid configuration'}
