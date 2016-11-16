import io
import os
import yaml
import jsonschema
from .. import exceptions


# Module API

def validate_job_conf(job_conf):
    """Validate job configuration.

    Raises:
        exceptions.InvalidJobConfiguration

    Returns:
        True

    """
    try:
        return _validate(job_conf, 'job-conf.yml')
    except jsonschema.ValidationError:
        raise exceptions.InvalidJobConfiguration()


def validate_validation_conf(validation_conf):
    """Validate the configuration for the validation task.

    Raises:
        exceptions.InvalidValidationConfiguration

    Returns:
        True

    """
    try:
        return _validate(validation_conf, 'validation-conf.yml')
    except jsonschema.ValidationError:
        raise exceptions.InvalidValidationConfiguration()


# Internal

def _validate(struct, schema):
    schema_path = os.path.join(
         os.path.dirname(__file__), '..', 'schemas', schema)
    schema = yaml.load(io.open(schema_path, encoding='utf-8'))
    jsonschema.validate(struct, schema)
    return True
