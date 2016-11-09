import dataset
from . import config


# Module API

database = dataset.connect(config.DATABASE_URL)
database.get_table('reports', primary_id='task_id', primary_type='String')
