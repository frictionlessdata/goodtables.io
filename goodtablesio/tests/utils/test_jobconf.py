import pytest
from goodtablesio import exceptions
from goodtablesio.utils.jobconf import make_validation_conf, parse_job_conf
from goodtablesio.utils.jobconf import verify_validation_conf, _verify_job_conf


# Tests

def test_create_validation_conf():
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

    job_conf = {
        'files': '*',
        'settings': {
            'error_limit': 1
        }
    }

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
    assert make_validation_conf(
        job_files, job_conf, job_base) == validation_conf


def test_create_validation_conf_no_base():
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

    job_conf = {
        'files': '*',
        'settings': {
            'error_limit': 1
        }
    }

    validation_conf = {
        'files': [
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
    assert make_validation_conf(
        job_files, job_conf) == validation_conf


def test_create_validation_conf_subdir():
    job_base = 'http://example.com'
    job_files = [
        'data/file.csv',
        'file.pdf',
    ]
    job_conf = {
        'files': '*'
    }

    validation_conf = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }

    assert make_validation_conf(
        job_files, job_conf, job_base) == validation_conf


def test_create_validation_conf_subdir_config():
    job_base = 'http://example.com'
    job_files = [
        'data/file.csv',
        'file.ods',
        'file.pdf',
    ]
    job_conf = {
        'files': 'data/*'
        }

    validation_conf = {
        'files': [
            {'source': 'http://example.com/data/file.csv'},
        ]
    }

    assert make_validation_conf(
        job_files, job_conf, job_base) == validation_conf


def test_create_validation_conf_subdir_granular():
    job_base = 'http://example.com'
    job_files = [
        'data/file.csv',
        'data/schema.json',
        'file.ods',
        'file.pdf',
    ]

    job_conf = {
        'files': [
            {
                'source': 'data/file.csv',
                'schema': 'data/schema.json',
                'delimiter': ';',
                'skip_rows': [1, 2, '#', '//']
            }
        ],
        'settings': {
            'order_fields': True
        }
    }

    validation_conf = {
        'files': [
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

    assert make_validation_conf(
        job_files, job_conf, job_base) == validation_conf


def test_create_validation_conf_default_job_conf():
    job_base = 'http://example.com'
    job_files = [
        'file1.csv',
        'file2.csv',
        'file.pdf',
    ]

    job_conf = None

    validation_conf = {
        'files': [
            {'source': 'http://example.com/file1.csv'},
            {'source': 'http://example.com/file2.csv'},
        ]
    }

    assert make_validation_conf(
        job_files, job_conf, job_base) == validation_conf


def test_parse_job_conf():
    job_conf_text = """
        files: '*'
        settings:
            error_limit: 1
    """

    job_conf = {
        'files': '*',
        'settings': {
            'error_limit': 1
        }
    }

    assert parse_job_conf(job_conf_text) == job_conf


def test_parse_job_conf_invalid():
    job_conf_text = """
        files: {}
    """
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert parse_job_conf(job_conf_text)


def test_parse_job_conf_invalid_text():
    job_conf_text = """
        aaa
    """
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert parse_job_conf(job_conf_text)


def test_parse_job_conf_invalid_yml():
    job_conf_text = """
        files: ][
    """
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert parse_job_conf(job_conf_text)


def test_parse_job_conf_invalid_none():
    job_conf_text = None
    assert parse_job_conf(job_conf_text) is None


def test_parse_job_conf_files_settings():
    job_conf_text = """
        files:
          - source: data/file.csv
            schema: data/schema.json
            delimiter: ';'
            skip_rows: [1, 2, '#', '//']
        settings:
            order_fields: true
    """
    job_conf = {
        'files': [
            {
                'source': 'data/file.csv',
                'schema': 'data/schema.json',
                'delimiter': ';',
                'skip_rows': [1, 2, '#', '//']
            }
        ],
        'settings': {
            'order_fields': True
        }
    }

    assert parse_job_conf(job_conf_text) == job_conf


def test_verify_job_conf():
    assert _verify_job_conf({
        'files': '*',
    })


def test_verify_job_conf_invalid():
    with pytest.raises(exceptions.InvalidJobConfiguration):
        assert _verify_job_conf({
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
