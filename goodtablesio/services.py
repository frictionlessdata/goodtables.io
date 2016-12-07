import dataset

from . import config


# Module API

database = dataset.connect(config.DATABASE_URL)
