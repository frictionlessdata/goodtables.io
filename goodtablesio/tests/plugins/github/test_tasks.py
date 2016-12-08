from mock import patch
from goodtablesio.plugins.github import tasks


# Tests

def test_get_job_base():
    actual = tasks._get_job_base('frictionlessdata', 'goodtables.io-example')
    expect = 'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master'  # noqa
    assert actual == expect


def test_get_job_files():
    actual = tasks._get_job_files('frictionlessdata', 'goodtables.io-example', 'd5be243487d9882d7f762e7fa04b36b900164a59')  # noqa
    expect = [
        'README.md',
        'data/invalid.csv',
        'goodtables.yml',
        'valid.csv',
    ]
    assert actual == expect


@patch.object(tasks, '_get_job_files_tree_api')
def test_get_job_files_fallback(_get_job_files_tree_api):
    _get_job_files_tree_api.return_value = None
    actual = tasks._get_job_files('frictionlessdata', 'goodtables.io-example', 'd5be243487d9882d7f762e7fa04b36b900164a59')  # noqa
    expect = [
        'README.md',
        'data/invalid.csv',
        'goodtables.yml',
        'valid.csv',
    ]
    assert actual == expect
