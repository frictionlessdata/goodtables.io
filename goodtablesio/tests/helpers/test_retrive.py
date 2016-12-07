import pytest

from goodtablesio import helpers
from goodtablesio.tests import factories


# Tests

@pytest.mark.usefixtures('db_cleanup')
def test_get_ids():
    factories.Job(job_id='id1')
    factories.Job(job_id='id2')

    assert helpers.get_job_ids() == ['id2', 'id1']
