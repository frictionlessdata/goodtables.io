import os
import yaml
import requests
from fnmatch import fnmatch
from .validate import validate_job_conf
from .. import config


# Module API

def prepare_job(job_conf_url, job_files):
    """Convert job configuration and job files to a validation configuration.

    Args:
        job_conf_url (url): URL to the job configuration file (goodtable.yml)
        job_files (url[]): Potential job files (not filtered, relative paths)

    Raises:
        exceptions.InvalidJobConfiguration

    Returns:
        validation_conf (dict): Configuration object to be used by the
            validation task

    This function is separate to make testing easier.
    """

    # Get base url and load job configuration
    base_url = job_conf_url.rsplit('/', 1)[0]
    yml_file = _load_file(job_conf_url)
    if yml_file:
        job_conf = yaml.load(yml_file)

        # Validate job configuration
        validate_job_conf(job_conf)

    else:
        job_conf = {'files': '*'}

    return _prepare_validation_conf(job_conf, job_files, base_url)


# Internal

def _prepare_validation_conf(job_conf, job_files, base_url):

    validation_conf = {}

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


def _load_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def _is_tabular_file(name):
    extension = os.path.splitext(name)[1]
    if extension and extension[1:].lower() in config.TABULAR_EXTENSIONS:
        return True
    return False
