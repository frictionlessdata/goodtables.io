from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from goodtablesio import config


def get_engine(engine_kwargs=None):

    engine_kwargs = engine_kwargs or {}

    return create_engine(config.DATABASE_URL, **engine_kwargs)


def make_db_session(engine=None, engine_kwargs=None):
    if not engine:
        engine = get_engine(engine_kwargs=engine_kwargs)

    return scoped_session(sessionmaker(bind=engine))


db_session = make_db_session()
