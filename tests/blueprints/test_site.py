from goodtablesio import helpers, services


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

    services.database['jobs'].delete()


def test_site_get_job_not_found(client):

    response = client.get('/job/xxx')

    assert response.status_code == 404
