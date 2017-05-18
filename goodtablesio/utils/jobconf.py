import io
import os
import yaml
import tabulator
import jsonschema
from fnmatch import fnmatch
from goodtablesio import settings
from goodtablesio import exceptions


# Module API

def make_validation_conf(job_conf_text, job_files, job_base=None):
    """Given a list of files and a job configuration (goodtables.yml),
        return the validation configuratio to be used by the validation
        task (goodtables)

    Raises:
        exceptions.InvalidJobConfiguration
        exceptions.InvalidValidationConfiguration

    Args:
        job_conf_text (str): Contents of the goodtables.yml file
        job_files (str[]): List of file paths, relative to job_base
        job_base (url): Base URL for file paths (optional)

    Returns:
        validation_conf (dict): Conf to be used by the validation task

    """
    validation_conf = {'source': []}

    # Parse, set defaults and verify job conf
    job_conf = _parse_job_conf(job_conf_text) or {}
    if not job_conf.get('files', job_conf.get('datapackages')):
        if 'datapackage.json' in job_files:
            job_conf['datapackages'] = ['datapackage.json']
        else:
            job_conf['files'] = '*'
    _verify_job_conf(job_conf)

    # Files: string
    if isinstance(job_conf.get('files'), str):
        pattern = job_conf['files']
        for name in job_files:
            if not _is_glob_supported_format(name, pattern):
                continue
            if not fnmatch(name, pattern):
                continue
            source = name
            if job_base:
                source = '/'.join([job_base, name])
            validation_conf['source'].append({
                'source': source,
            })

    # Files: array of objects
    elif isinstance(job_conf.get('files'), list):
        for item in job_conf['files']:
            if item['source'] in job_files:
                item['source'] = '/'.join([job_base, item['source']])
                if ('schema' in item
                        and not item['schema'].startswith('http')
                        and job_base):
                    item['schema'] = '/'.join(
                        [job_base, item['schema']])
                validation_conf['source'].append(item)

    # Datapackages
    if 'datapackages' in job_conf:
        for name in job_conf['datapackages']:
            source = name
            if job_base:
                source = '/'.join([job_base, name])
            validation_conf['source'].append({
                'source': source,
                'preset': 'datapackage',
            })

    # Settings
    if 'settings' in job_conf:
        validation_conf['settings'] = job_conf['settings']

    # Verify validation conf
    verify_validation_conf(validation_conf)

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


def _is_glob_supported_format(name, pattern):
    """Check if this file is supported
    """
    for format in settings.GLOB_EXCLUDED_FORMATS:
        if format in pattern:
            continue
        if format == os.path.splitext(name.lower())[1][1:]:
            return False
    try:
        tabulator.validate(name)
    except tabulator.exceptions.TabulatorException:
        return False
    return True
