import pytest
from unittest.mock import patch
from goodtablesio import helpers


# Tests

def test_prepare_task(load_file):
    task_conf = [
        'http://example.com/task_conf.yml',
        """
        files: '*'
        settings:
            error_limit: 1
        """
    ]
    task_files = [
        'file.csv',
        'file.pdf',
    ]
    task_desc = {
        'files': [
            {'source': 'http://example.com/file.csv'},
        ],
        'settings': {
            'error_limit': 1,
        }
    }
    load_file.return_value = task_conf[1]
    assert helpers.prepare_task(task_conf[0], task_files) == task_desc


def test_prepare_task_subdir(load_file):
    task_conf = [
        'http://example.com/task_conf.yml',
        """
        files: '*'
        """
    ]
    task_files = [
        'data/file.csv',
        'file.pdf',
    ]
    task_desc = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    load_file.return_value = task_conf[1]
    assert helpers.prepare_task(task_conf[0], task_files) == task_desc


def test_prepare_task_subdir_config(load_file):
    task_conf = [
        'http://example.com/task_conf.yml',
        """
        files: 'data/*'
        """
    ]
    task_files = [
        'data/file.csv',
        'file.ods',
        'file.pdf',
    ]
    task_desc = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }
    load_file.return_value = task_conf[1]
    assert helpers.prepare_task(task_conf[0], task_files) == task_desc


def test_prepare_task_subdir_granular(load_file):
    task_conf = [
        'http://example.com/task_conf.yml',
        """
        files:
          - source: data/file.csv
            schema: data/schema.json
            delimiter: ';'
        settings:
            order_fields: true
        """
    ]
    task_files = [
        'data/file.csv',
        'data/schema.json',
        'file.ods',
        'file.pdf',
    ]
    task_desc = {
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
    load_file.return_value = task_conf[1]
    assert helpers.prepare_task(task_conf[0], task_files) == task_desc


def test_prepare_task_invalid(load_file):
    task_conf = [
        'http://example.com/task_conf.yml',
        """
        files: {}
        """
    ]
    load_file.return_value = task_conf[1]
    with pytest.raises(Exception):
        assert helpers.prepare_task(task_conf[0], [])


# Fixtures

@pytest.fixture
def load_file():
    return patch('goodtablesio.helpers.prepare._load_file').start()
