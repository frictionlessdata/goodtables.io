import datetime

import pytest

from goodtablesio import models
from goodtablesio.tests import factories
from goodtablesio.services import database


pytestmark = pytest.mark.usefixtures('session_cleanup')


def test_create_job_outputs_dict():

    job = models.job.create({'id': 'my-id'})

    assert job['id'] == 'my-id'
    assert job['status'] == 'created'
    assert job['plugin_name'] == 'api'
    assert job['plugin_conf'] is None
    assert job['created']
    assert job['finished'] is None
    assert job['report'] is None
    assert job['error'] is None


def test_create_job_params_outputs_dict():

    params = {
        'id': 'my-id',
        'plugin_name': 'my-plugin',
        'plugin_conf': {'some': 'conf'}
    }

    job = models.job.create(params)

    assert job['id'] == 'my-id'
    assert job['status'] == 'created'
    assert job['plugin_name'] == 'my-plugin'
    assert job['plugin_conf'] == {'some': 'conf'}
    assert job['created']
    assert job['finished'] is None
    assert job['report'] is None
    assert job['error'] is None


def test_create_job_stored_in_db():

    params = {
        'id': 'my-id',
        'plugin_name': 'my-plugin',
        'plugin_conf': {'some': 'conf'}
    }

    models.job.create(params)

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    job = database['session'].query(models.job.Job).get('my-id')

    assert job

    assert job.id == 'my-id'
    assert job.status == 'created'
    assert job.plugin_name == 'my-plugin'
    assert job.plugin_conf == {'some': 'conf'}
    assert job.created
    assert job.finished is None
    assert job.report is None
    assert job.error is None


def test_update_job_outputs_dict():

    job = factories.Job()

    report = {'nice': 'csv'}
    finished = datetime.datetime.utcnow()
    params = {
        'id': job.id,
        'status': 'success',
        'report': report,
        'finished': finished,
    }

    updated_job = models.job.update(params)

    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'success'
    assert updated_job['plugin_name'] == 'api'
    assert updated_job['plugin_conf'] is None
    assert updated_job['created']
    assert updated_job['finished'].replace(tzinfo=None) == finished
    assert updated_job['report'] == report
    assert updated_job['error'] is None


def test_update_job_stored_in_db():

    job = factories.Job()

    report = {'nice': 'csv'}
    finished = datetime.datetime.utcnow()
    params = {
        'id': job.id,
        'status': 'success',
        'report': report,
        'finished': finished,
    }

    models.job.update(params)

    # Make sure that we are not checking the cached object in the session
    database['session'].remove()

    updated_job = database['session'].query(models.job.Job).get(job.id)

    assert updated_job

    assert updated_job.id == job.id
    assert updated_job.status == 'success'
    assert updated_job.plugin_name == 'api'
    assert updated_job.plugin_conf is None
    assert updated_job.created
    assert updated_job.finished.replace(tzinfo=None) == finished
    assert updated_job.report == report
    assert updated_job.error is None


def test_update_job_no_id_raises_value_error():
    with pytest.raises(ValueError):
        assert models.job.update({})


def test_update_job_not_found_raises_value_error():
    with pytest.raises(ValueError):
        assert models.job.update({'id': 'not-found'})


def test_get_job_outputs_dict():

    # Actually save it to the DB so we can test retrieving it
    job_db = factories.Job(_save_in_db=True).to_dict()

    database['session'].remove()

    job = models.job.get(job_db['id'])

    assert job['id'] == job_db['id']
    assert job['status'] == job_db['status']
    assert job['plugin_name'] == job_db['plugin_name']
    assert job['plugin_conf'] == job_db['plugin_conf']
    assert job['created'] == job_db['created']
    assert job['finished'] == job_db['finished']
    assert job['report'] == job_db['report']
    assert job['error'] == job_db['error']


def test_get_job_not_found_outputs_none():

    assert models.job.get('not-found') is None


def test_get_all():
    job1 = factories.Job()
    job2 = factories.Job()
    job3 = factories.Job()

    all_jobs = models.job.get_all()

    assert len(all_jobs) == 3

    assert all_jobs == [job3.to_dict(), job2.to_dict(), job1.to_dict()]


def test_get_ids():
    job1 = factories.Job()
    job2 = factories.Job()

    assert models.job.get_ids() == [job2.id, job1.id]
