import datetime
from unittest import mock

import pytest
from celery import Celery

from goodtablesio import tasks, exceptions, models
from goodtablesio.tests import factories


pytestmark = pytest.mark.usefixtures('session_cleanup')


@mock.patch('goodtables.inspector.Inspector.inspect')
def test_tasks_validate(_inspect):

    # We need to save it on the DB so the session used by the tasks can find it
    job = factories.Job(_save_in_db=True)

    mock_report = {'valid': True, 'errors': []}
    _inspect.return_value = mock_report

    validation_conf = {'files': ['file1', 'file2'], 'settings': {}}
    tasks.validate(validation_conf, job_id=job.id)

    _inspect.assert_called_with(validation_conf['files'], preset='tables')

    jobs = models.job.get_all()

    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['report'] == mock_report
    assert isinstance(updated_job['finished'], datetime.datetime)


def test_JobTask_on_failure_invalid_job_conf():

    # Prepare things
    job = factories.Job(_save_in_db=True)
    app = Celery('app')
    app.conf['task_always_eager'] = True

    # Prepare and call task
    @app.task(base=tasks.JobTask)
    def task(job_id):
        raise exceptions.InvalidJobConfiguration()
    task.s(job_id=job.id).delay()

    # Assert errored job
    jobs = models.job.get_all()
    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'error'
    assert updated_job['error'] == {'message': 'Invalid job configuration'}
    assert isinstance(updated_job['finished'], datetime.datetime)


def test_JobTask_on_failure_invalid_validation_conf():

    # Prepare things
    job = factories.Job(_save_in_db=True)
    app = Celery('app')
    app.conf['task_always_eager'] = True

    # Prepare and call task
    @app.task(base=tasks.JobTask)
    def task(job_id):
        raise exceptions.InvalidValidationConfiguration()
    task.s(job_id=job.id).delay()

    # Assert errored job
    jobs = models.job.get_all()
    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'error'
    assert updated_job['error'] == {'message': 'Invalid validation configuration'}
    assert isinstance(updated_job['finished'], datetime.datetime)
