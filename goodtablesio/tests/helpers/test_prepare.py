import pytest
from unittest.mock import patch
from goodtablesio import helpers, exceptions


# Tests

def test_create_validation_conf(load_file):
    job_base = 'http://example.com'
    job_files = [
        'file.csv',
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
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    load_file.return_value = job_conf_text
    assert helpers.create_validation_conf(job_base, job_files) == validation_conf


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
    assert helpers.create_validation_conf(job_base, job_files) == validation_conf


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
    assert helpers.create_validation_conf(job_base, job_files) == validation_conf


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
        settings:
            order_fields: true
    """
    validation_conf = {
        'files': [
            {
                'source': 'http://example.com/data/file.csv',
                'schema': 'http://example.com/data/schema.json',
                'delimiter': ';',
            },
        ],
        'settings': {
            'order_fields': True,
        }
    }
    load_file.return_value = job_conf_text
    assert helpers.create_validation_conf(job_base, job_files) == validation_conf


def test_create_validation_conf_invalid(load_file):
    job_base = 'http://example.com'
    job_conf_text = """
        files: {}
    """
    load_file.return_value = job_conf_text
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert helpers.create_validation_conf(job_base, [])


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
    assert helpers.create_validation_conf(job_base, job_files) == validation_conf


# Fixtures

@pytest.fixture
def load_file():
    yield patch('goodtablesio.helpers.prepare._load_file').start()
    patch.stopall()
