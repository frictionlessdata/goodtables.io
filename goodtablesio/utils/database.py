from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from goodtablesio import settings


# Module API

def create_session(**params):
    engine = create_engine(settings.DATABASE_URL, **params)
    session = scoped_session(sessionmaker(bind=engine))
    return session
