import dataset

from . import config


# Module API

database = dataset.connect(config.DATABASE_URL)
database.get_table('jobs', primary_id='job_id', primary_type='String')

database['jobs'].drop()
database.get_table('jobs', primary_id='job_id', primary_type='String')
