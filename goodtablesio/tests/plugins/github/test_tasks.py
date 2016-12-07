# pylama:skip=1
from goodtablesio.plugins.github import tasks


# Tests

def test_get_job_urls():
    assert tasks._get_job_urls('frictionlessdata', 'goodtables.io-example') == (
        'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master/goodtables.yml',
        [
            'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master/README.md',
            'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master/data/invalid.csv',
            'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master/goodtables.yml',
            'https://raw.githubusercontent.com/frictionlessdata/goodtables.io-example/master/valid.csv',
        ]
    )
