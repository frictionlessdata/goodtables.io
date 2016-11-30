import pytest
from unittest.mock import patch
from goodtablesio import helpers, exceptions


# Tests

def test_prepare_job(load_file):
    job_conf = [
        'http://example.com/job_conf.yml',
        """
        files: '*'
        settings:
            error_limit: 1
        """
    ]
    job_files = [
        'file.csv',
        'file.pdf',
    ]
    validation_conf = {
        'files': [
            {'source': 'http://example.com/file.csv'},
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    load_file.return_value = job_conf[1]
    assert helpers.prepare_job(job_conf[0], job_files) == validation_conf


def test_prepare_job_subdir(load_file):
    job_conf = [
        'http://example.com/job_conf.yml',
        """
        files: '*'
        """
    ]
    job_files = [
        'data/file.csv',
        'file.pdf',
    ]
    validation_conf = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    load_file.return_value = job_conf[1]
    assert helpers.prepare_job(job_conf[0], job_files) == validation_conf


def test_prepare_job_subdir_config(load_file):
    job_conf = [
        'http://example.com/job_conf.yml',
        """
        files: 'data/*'
        """
    ]
    job_files = [
        'data/file.csv',
        'file.ods',
        'file.pdf',
    ]
    validation_conf = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    load_file.return_value = job_conf[1]
    assert helpers.prepare_job(job_conf[0], job_files) == validation_conf


def test_prepare_job_subdir_granular(load_file):
    job_conf = [
        'http://example.com/job_conf.yml',
        """
        files:
          - source: data/file.csv
            schema: data/schema.json
            delimiter: ';'
        settings:
            order_fields: true
        """
    ]
    job_files = [
        'data/file.csv',
        'data/schema.json',
        'file.ods',
        'file.pdf',
    ]
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
    load_file.return_value = job_conf[1]
    assert helpers.prepare_job(job_conf[0], job_files) == validation_conf


def test_prepare_job_invalid(load_file):
    job_conf = [
        'http://example.com/job_conf.yml',
        """
        files: {}
        """
    ]
    load_file.return_value = job_conf[1]
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert helpers.prepare_job(job_conf[0], [])


def test_prepare_job_goodtables_yml_not_found(load_file):
    job_conf_url = 'http://example.com/job_conf.yml'
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
    assert helpers.prepare_job(job_conf_url, job_files) == validation_conf


# Fixtures

@pytest.fixture
def load_file():
    yield patch('goodtablesio.helpers.prepare._load_file').start()
    patch.stopall()
