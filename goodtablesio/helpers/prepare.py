import os
import yaml
import requests
from fnmatch import fnmatch
from .validate import validate_job_conf
from .. import exceptions
from .. import config


# Module API

def create_validation_conf(job_base, job_files):
    """Create validation configuration from job base url and file paths.

    Args:
        job_base (url): url base for job file paths
        job_files (str[]): relative to base job file paths

    Raises:
        exceptions.InvalidJobConfiguration

    Returns:
        validation_conf (dict): Configuration object to be used by the
            validation task

    This function is pure to make testing easier.

    """
    job_conf = _load_job_conf(job_base)
    validate_job_conf(job_conf)
    validation_conf = _make_validation_conf(job_base, job_files, job_conf)
    return validation_conf


# Internal


def _load_job_conf(job_base):
    job_conf = {'files': '*'}
    url = '/'.join([job_base, 'goodtables.yml'])
    text = _load_file(url)
    if text is not None:
        try:
            job_conf = yaml.safe_load(text)
        except Exception:
            raise exceptions.InvalidJobConfiguration()
    return job_conf


def _make_validation_conf(job_base, job_files, job_conf):
    validation_conf = {}

    # Wild-card syntax
    validation_conf['files'] = []
    if isinstance(job_conf['files'], str):
        pattern = job_conf['files']
        for name in job_files:
            if not _is_tabular_file(name):
                continue
            if fnmatch(name, pattern):
                source = '/'.join([job_base, name])
                validation_conf['files'].append({
                    'source': source,
                })

    # Granular syntax
    else:
        for item in job_conf['files']:
            if item['source'] in job_files:
                item['source'] = '/'.join([job_base, item['source']])
                if 'schema' in item:
                    if not item['schema'].startswith('http'):
                        item['schema'] = '/'.join([job_base, item['schema']])
                validation_conf['files'].append(item)

    # Copy settings
    if 'settings' in job_conf:
        validation_conf['settings'] = job_conf['settings']

    return validation_conf


def _load_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def _is_tabular_file(name):
    extension = os.path.splitext(name)[1]
    if extension and extension[1:].lower() in config.TABULAR_EXTENSIONS:
        return True
    return False
