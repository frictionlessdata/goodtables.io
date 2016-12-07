from goodtablesio.plugins.github import tasks


# Tests

def test_get_job_base():
    actual = tasks._get_job_base('frictionlessdata', 'goodtables.io-example')
    expect = 'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master'  # noqa
    assert actual == expect


def test_get_job_files():
    actual = tasks._get_job_files('frictionlessdata', 'goodtables.io-example')
    expect = [
        'README.md',
        'data/invalid.csv',
        'goodtables.yml',
        'valid.csv',
    ]
    assert actual == expect
