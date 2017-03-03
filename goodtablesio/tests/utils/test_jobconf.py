import pytest
from goodtablesio import exceptions
from goodtablesio.utils.jobconf import make_validation_conf, verify_validation_conf


# Tests

def test_make_validation_conf():
    job_conf_text = """
    files: '*'
    settings:
      error_limit: 1
    """
    job_files = [
        'file.csv',
        'file.json',
        'file.jsonl',
        'file.ndjson',
        'file.tsv',
        'file.xls',
        'file.ods',
        'file.pdf',
        'goodtables.yml',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file.csv'},
            {'source': 'http://example.com/file.json'},
            {'source': 'http://example.com/file.jsonl'},
            {'source': 'http://example.com/file.ndjson'},
            {'source': 'http://example.com/file.tsv'},
            {'source': 'http://example.com/file.xls'},
            {'source': 'http://example.com/file.ods'},
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_no_base():
    job_conf_text = """
    files: '*'
    settings:
      error_limit: 1
    """
    job_files = [
        'file.csv',
        'file.json',
        'file.jsonl',
        'file.ndjson',
        'file.tsv',
        'file.xls',
        'file.ods',
        'file.pdf',
        'goodtables.yml',
    ]
    validation_conf = {
        'source': [
            {'source': 'file.csv'},
            {'source': 'file.json'},
            {'source': 'file.jsonl'},
            {'source': 'file.ndjson'},
            {'source': 'file.tsv'},
            {'source': 'file.xls'},
            {'source': 'file.ods'},
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    assert make_validation_conf(job_conf_text, job_files) == validation_conf


def test_make_validation_conf_subdir():
    job_conf_text = """
    files: '*'
    """
    job_files = [
        'data/file.csv',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }

    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_subdir_config():
    job_conf_text = """
    files: data/*
    """
    job_files = [
        'data/file.csv',
        'file.ods',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }

    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_subdir_granular():
    job_conf_text = """
    files:
      - source: data/file.csv
        schema: data/schema.json
        delimiter: ';'
        skip_rows: [1, 2, '#', '//']
    settings:
      order_fields: True
    """
    job_files = [
        'data/file.csv',
        'data/schema.json',
        'file.ods',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {
                'source': 'http://example.com/data/file.csv',
                'schema': 'http://example.com/data/schema.json',
                'delimiter': ';',
                'skip_rows': [1, 2, '#', '//'],
            },
        ],
        'settings': {
            'order_fields': True,
        }
    }

    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_default_job_conf():
    job_conf_text = None
    job_files = [
        'file1.csv',
        'file2.csv',
        'file.pdf',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file1.csv'},
            {'source': 'http://example.com/file2.csv'},
        ]
    }

    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_datapackages():
    job_conf_text = """
    datapackages:
      - datapackage1.json
      - datapackage2.json
    """
    job_files = [
        'datapackage1.json',
        'datapackage2.json',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/datapackage1.json', 'preset': 'datapackage'},
            {'source': 'http://example.com/datapackage2.json', 'preset': 'datapackage'},
        ]
    }

    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_make_validation_conf_files_and_datapackages():
    job_conf_text = """
    files: '*.csv'
    datapackages:
      - datapackage1.json
      - datapackage2.json
    """
    job_files = [
        'file1.csv',
        'file2.csv',
        'datapackage1.json',
        'datapackage2.json',
    ]
    job_base = 'http://example.com'
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file1.csv'},
            {'source': 'http://example.com/file2.csv'},
            {'source': 'http://example.com/datapackage1.json', 'preset': 'datapackage'},
            {'source': 'http://example.com/datapackage2.json', 'preset': 'datapackage'},
        ]
    }

    assert make_validation_conf(job_conf_text, job_files, job_base) == validation_conf


def test_verify_validation_conf():
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file.csv'},
            {'source': 'http://example.com/datapackage.json', 'preset': 'datapackage'},
        ]
    }

    assert verify_validation_conf(validation_conf)


def test_verify_validation_conf_invalid_bad_preset():
    validation_conf = {
        'source': [
            {'source': 'http://example.com/file.csv', 'preset': 'bad-preset'},
        ]
    }

    with pytest.raises(exceptions.InvalidValidationConfiguration):
        verify_validation_conf(validation_conf)


def test_verify_validation_conf_invalid_empty_source():
    validation_conf = {
        'source': []
    }

    with pytest.raises(exceptions.InvalidValidationConfiguration):
        verify_validation_conf(validation_conf)
