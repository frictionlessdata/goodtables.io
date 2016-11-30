import dataset
from sqlalchemy.dialects.postgresql import JSONB

from . import config


# Module API

database = dataset.connect(config.DATABASE_URL)
database.get_table('jobs', primary_id='job_id', primary_type='String')

# TODO: get rid of this after #33
database['jobs'].create_column('plugin_conf', JSONB)
