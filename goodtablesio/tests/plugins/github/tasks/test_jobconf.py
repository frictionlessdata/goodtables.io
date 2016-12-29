from unittest.mock import patch
from goodtablesio.plugins.github.tasks import jobconf

# Constants

OWNER = 'frictionlessdata'
REPO = 'goodtables.io-example'
SHA = 'd5be243487d9882d7f762e7fa04b36b900164a59'


# Tests

def test_get_job_base():
    actual = jobconf._get_job_base(OWNER, REPO, SHA)
    expect = 'https://raw.githubusercontent.com/frictionlessdata/'
    expect += 'goodtables.io-example/d5be243487d9882d7f762e7fa04b36b900164a59'
    assert actual == expect


def test_get_job_files():
    actual = jobconf._get_job_files(OWNER, REPO, SHA)
    expect = [
        'README.md',
        'data/invalid.csv',
        'goodtables.yml',
        'valid.csv',
    ]
    assert actual == expect


@patch.object(jobconf, '_get_job_files_tree_api')
def test_get_job_files_fallback(_get_job_files_tree_api):
    _get_job_files_tree_api.return_value = None
    actual = jobconf._get_job_files(OWNER, REPO, SHA)
    expect = [
        'README.md',
        'data/invalid.csv',
        'goodtables.yml',
        'valid.csv',
    ]
    assert actual == expect
