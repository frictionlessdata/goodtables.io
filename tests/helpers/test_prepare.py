from unittest.mock import patch
from goodtablesio import helpers


@patch('goodtablesio.helpers.prepare._load_file')
def test_prepare_task(load_file):

    task_conf = [
        'http://example.com/task_conf.yml',
        """
        files: '*'
        """
    ]
    task_files = [
        'file.csv',
        'file.pdf',
    ]
    task_desc = {
        'files': [
            {'source': 'http://example.com/file.csv'},
        ]
    }

    load_file.return_value = task_conf[1]
    assert helpers.prepare_task(task_conf[0], task_files) == task_desc
