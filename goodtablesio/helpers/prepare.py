import os
import yaml
import requests
from fnmatch import fnmatch
from .validate import validate_task_conf
from .. import config


# Module API

def prepare_task(task_conf, task_files):
    """Convert task configuration and task files to task description.

    Args:
        task_conf (url): task configuration
        task_files (url[]): task files (not filtered, relative paths)

    Raises:
        exceptions.InvalidTaskConfiguration

    Returns:
        task_desc (dict): task descriptor

    This is a pure function for better testing ability
    of this important chunk of application logic.

    """
    task_desc = {}

    # Get base url and load task configuration
    base_url = task_conf.rsplit('/', 1)[0]
    task_conf = yaml.load(_load_file(task_conf))

    # Validate task configuration
    validate_task_conf(task_conf)

    # Wild-card syntax
    task_desc['files'] = []
    if isinstance(task_conf['files'], str):
        pattern = task_conf['files']
        for name in task_files:
            if not _is_tabular_file(name):
                continue
            if fnmatch(name, pattern):
                source = '/'.join([base_url, name])
                task_desc['files'].append({
                    'source': source,
                })

    # Granular syntax
    else:
        for item in task_conf['files']:
            if item['source'] in task_files:
                item['source'] = '/'.join([base_url, item['source']])
                if 'schema' in item:
                    if not item['schema'].startswith('http'):
                        item['schema'] = '/'.join([base_url, item['schema']])
                task_desc['files'].append(item)

    # Copy settings
    if 'settings' in task_conf:
        task_desc['settings'] = task_conf['settings']

    return task_desc


# Internal

def _load_file(url):
    response = requests.get(url)
    return response.text


def _is_tabular_file(name):
    extension = os.path.splitext(name)[1]
    if extension and extension[1:].lower() in config.TABULAR_EXTENSIONS:
        return True
    return False
