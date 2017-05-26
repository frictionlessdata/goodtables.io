import pytest
import datetime
from celery import Celery
from goodtablesio import exceptions, models
from goodtablesio.tasks.base import JobTask, InternalJobTask
from goodtablesio.tests import factories
pytestmark = pytest.mark.usefixtures('session_cleanup')


# Tests

def test_JobTask_on_failure_invalid_job_conf(celery_app):

    # Prepare things
    job = factories.Job(_save_in_db=True)

    # Prepare and call task
    @celery_app.task(base=JobTask)
    def task(job_id):
        raise exceptions.InvalidJobConfiguration('message')
    task.delay(job_id=job.id)

    # Assert errored job
    jobs = models.job.find()
    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'error'
    assert updated_job['error'] == {'message': 'message'}
    assert isinstance(updated_job['finished'], datetime.datetime)


def test_JobTask_on_failure_invalid_validation_conf(celery_app):

    # Prepare things
    job = factories.Job(_save_in_db=True)

    # Prepare and call task
    @celery_app.task(base=JobTask)
    def task(job_id):
        raise exceptions.InvalidValidationConfiguration('message')
    task.delay(job_id=job.id)

    # Assert errored job
    jobs = models.job.find()
    assert len(jobs) == 1

    updated_job = jobs[0]
    assert updated_job['id'] == job.id
    assert updated_job['status'] == 'error'
    assert updated_job['error'] == {'message': 'message'}
    assert isinstance(updated_job['finished'], datetime.datetime)


def test_InternalJobTask_on_failure_exception(celery_app):

    # Prepare things
    job = factories.InternalJob(_save_in_db=True)

    # Prepare and call task
    @celery_app.task(base=InternalJobTask)
    def task(job_id):
        raise RuntimeError('bad')
    task.delay(job_id=job.id)

    # Assert errored task
    assert job.status == 'error'
    assert job.error == {'message': 'Internal error'}
    assert job.finished


# Fixtures

@pytest.fixture
def celery_app():
    app = Celery('app')
    app.conf['task_always_eager'] = True
    return app
