import pytest
from unittest.mock import patch
from goodtablesio import exceptions
from goodtablesio.utils.jobconf import create_validation_conf
from goodtablesio.utils.jobconf import verify_validation_conf, verify_job_conf


# Tests

def test_create_validation_conf(load_file):
    job_base = 'http://example.com'
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
    job_conf_text = """
        files: '*'
        settings:
            error_limit: 1
    """
    validation_conf = {
        'files': [
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
    load_file.return_value = job_conf_text
    assert create_validation_conf(job_base, job_files) == validation_conf


def test_create_validation_conf_subdir(load_file):
    job_base = 'http://example.com'
    job_files = [
        'data/file.csv',
        'file.pdf',
    ]
    job_conf_text = """
        files: '*'
    """
    validation_conf = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    load_file.return_value = job_conf_text
    assert create_validation_conf(job_base, job_files) == validation_conf


def test_create_validation_conf_subdir_config(load_file):
    job_base = 'http://example.com'
    job_files = [
        'data/file.csv',
        'file.ods',
        'file.pdf',
    ]
    job_conf_text = """
        files: 'data/*'
    """
    validation_conf = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    load_file.return_value = job_conf_text
    assert create_validation_conf(job_base, job_files) == validation_conf


def test_create_validation_conf_subdir_granular(load_file):
    job_base = 'http://example.com'
    job_files = [
        'data/file.csv',
        'data/schema.json',
        'file.ods',
        'file.pdf',
    ]
    job_conf_text = """
        files:
          - source: data/file.csv
            schema: data/schema.json
            delimiter: ';'
            skipRows: [1, 2, '#', '//']
        settings:
            order_fields: true
    """
    validation_conf = {
        'files': [
            {
                'source': 'http://example.com/data/file.csv',
                'schema': 'http://example.com/data/schema.json',
                'delimiter': ';',
                'skipRows': [1, 2, '#', '//'],
            },
        ],
        'settings': {
            'order_fields': True,
        }
    }
    load_file.return_value = job_conf_text
    assert create_validation_conf(job_base, job_files) == validation_conf


def test_create_validation_conf_invalid(load_file):
    job_base = 'http://example.com'
    job_conf_text = """
        files: {}
    """
    load_file.return_value = job_conf_text
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert create_validation_conf(job_base, [])


def test_create_validation_conf_goodtables_yml_not_found(load_file):
    job_base = 'http://example.com'
    job_files = [
        'file1.csv',
        'file2.csv',
        'file.pdf',
    ]
    validation_conf = {
        'files': [
            {'source': 'http://example.com/file1.csv'},
            {'source': 'http://example.com/file2.csv'},
        ]
    }
    load_file.return_value = None
    assert create_validation_conf(job_base, job_files) == validation_conf


def test_verify_job_conf():
    assert verify_job_conf({
        'files': '*',
    })


def test_verify_job_conf_invalid():
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert verify_job_conf({
            'files': ['*'],
        })


def test_verify_validation_conf():
    assert verify_validation_conf({
        'files': [{'source': 'path.csv'}],
    })


def test_verify_validation_conf_invalid():
    with pytest.raises(exceptions.InvalidValidationConfiguration):
        assert verify_validation_conf({
            'files': ['*'],
        })


# Fixtures

@pytest.fixture
def load_file():
    yield patch('goodtablesio.utils.jobconf._load_file').start()
    patch.stopall()
