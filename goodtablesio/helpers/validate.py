import io
import os
import yaml
import jsonschema


# Module API

def validate_task_conf(task_conf):
    return _validate(task_conf, 'task-conf.yml')


def validate_task_desc(task_desc):
    return _validate(task_desc, 'task-desc.yml')


# Internal

def _validate(struct, schema):
    schema_path = os.path.join(
         os.path.dirname(__file__), '..', 'schemas', schema)
    schema = yaml.load(io.open(schema_path, encoding='utf-8'))
    jsonschema.validate(struct, schema)
    return True
