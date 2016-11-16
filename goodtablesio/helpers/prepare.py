import os
import yaml
import requests
from fnmatch import fnmatch
from .validate import validate_job_conf
from .. import config


# Module API

def prepare_job(job_conf, job_files):
    """Convert job configuration and job files to a validation configuration.

    Args:
        job_conf (url): URL to the job configuration file (goodtable.yml)
        job_files (url[]): Potential job files (not filtered, relative paths)

    Raises:
        exceptions.InvalidJobConfiguration

    Returns:
        validation_conf (dict): Configuration object to be used by the
            validation task

    This function is separate to make testing easier.
    """
    validation_conf = {}

    # Get base url and load job configuration
    base_url = job_conf.rsplit('/', 1)[0]
    job_conf = yaml.load(_load_file(job_conf))

    # Validate job configuration
    validate_job_conf(job_conf)

    # Wild-card syntax
    validation_conf['files'] = []
    if isinstance(job_conf['files'], str):
        pattern = job_conf['files']
        for name in job_files:
            if not _is_tabular_file(name):
                continue
            if fnmatch(name, pattern):
                source = '/'.join([base_url, name])
                validation_conf['files'].append({
                    'source': source,
                })

    # Granular syntax
    else:
        for item in job_conf['files']:
            if item['source'] in job_files:
                item['source'] = '/'.join([base_url, item['source']])
                if 'schema' in item:
                    if not item['schema'].startswith('http'):
                        item['schema'] = '/'.join([base_url, item['schema']])
                validation_conf['files'].append(item)

    # Copy settings
    if 'settings' in job_conf:
        validation_conf['settings'] = job_conf['settings']

    return validation_conf


# Internal

def _load_file(url):
    response = requests.get(url)
    return response.text


def _is_tabular_file(name):
    extension = os.path.splitext(name)[1]
    if extension and extension[1:].lower() in config.TABULAR_EXTENSIONS:
        return True
    return False
