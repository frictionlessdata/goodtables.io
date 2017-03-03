import io
import os
import yaml
import jsonschema
from fnmatch import fnmatch
from tabulator import Stream
from goodtablesio import exceptions


# Module API

def make_validation_conf(job_conf_text, job_files, job_base=None):
    """Given a list of files and a job configuration (goodtables.yml),
        return the validation configuratio to be used by the validation
        task (goodtables)

    Args:
        job_conf_text (str): Contents of the goodtables.yml file
        job_files (str[]): List of file paths, relative to job_base
        job_base (url): Base URL for file paths (optional)

    Returns:
        validation_conf (dict): Configuration object to be used by the
            validation task

    """
    job_conf = _parse_job_conf(job_conf_text) or {'files': '*'}
    validation_conf = {}

    # Wild-card syntax
    validation_conf['files'] = []
    if isinstance(job_conf['files'], str):
        pattern = job_conf['files']
        for name in job_files:
            if not Stream.test(name):
                continue
            if fnmatch(name, pattern):
                if job_base:
                    source = '/'.join([job_base, name])
                else:
                    source = name
                validation_conf['files'].append({
                    'source': source,
                })

    # Granular syntax
    else:
        for item in job_conf['files']:
            if item['source'] in job_files:
                item['source'] = '/'.join([job_base, item['source']])
                if ('schema' in item
                        and not item['schema'].startswith('http')
                        and job_base):
                    item['schema'] = '/'.join(
                        [job_base, item['schema']])
                validation_conf['files'].append(item)

    # Copy settings
    if 'settings' in job_conf:
        validation_conf['settings'] = job_conf['settings']

    return validation_conf


def verify_validation_conf(validation_conf):
    """Verify conf of the validation task.

    Raises:
        exceptions.InvalidValidationConfiguration

    Returns:
        True

    """
    try:
        return _verify_conf(validation_conf, 'validation-conf.yml')
    except jsonschema.ValidationError:
        raise exceptions.InvalidValidationConfiguration()


# Internal


def _parse_job_conf(contents):
    """Parse and verify job conf.
    """
    job_conf = None
    if contents:
        try:
            job_conf = yaml.safe_load(contents)
        except yaml.YAMLError as exception:
            raise exceptions.InvalidJobConfiguration(
                'Invalid YAML file: {}'.format(exception))
        _verify_job_conf(job_conf)
    return job_conf


def _verify_job_conf(job_conf):
    """Verify job conf.
    """
    try:
        return _verify_conf(job_conf, 'job-conf.yml')
    except jsonschema.ValidationError:
        raise exceptions.InvalidJobConfiguration()


def _verify_conf(conf, schema):
    """Verify conf by json schema.
    """
    schema_path = os.path.join(
         os.path.dirname(__file__), '..', 'schemas', schema)
    schema = yaml.load(io.open(schema_path, encoding='utf-8'))
    jsonschema.validate(conf, schema)
    return True
