import io
import os
import yaml
import jsonschema
from .. import exceptions


# Module API

def validate_task_conf(task_conf):
    """Validate task configuration.

    Raises:
        exceptions.InvalidTaskConfiguration

    Returns:
        True

    """
    try:
        return _validate(task_conf, 'task-conf.yml')
    except jsonschema.ValidationError:
        raise exceptions.InvalidTaskConfiguration()


def validate_task_desc(task_desc):
    """Validate task descriptor.

    Raises:
        exceptions.InvalidTaskDescriptor

    Returns:
        True

    """
    try:
        return _validate(task_desc, 'task-desc.yml')
    except jsonschema.ValidationError:
        raise exceptions.InvalidTaskDescriptor()


# Internal

def _validate(struct, schema):
    schema_path = os.path.join(
         os.path.dirname(__file__), '..', 'schemas', schema)
    schema = yaml.load(io.open(schema_path, encoding='utf-8'))
    jsonschema.validate(struct, schema)
    return True
