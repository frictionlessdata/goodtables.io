from functools import wraps
import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

from goodtablesio.services import db_session as default_db_session


Base = declarative_base()


class BaseModelMixin(object):

    def to_dict(self):
        '''Get any model object and represent it as a dict'''

        out = {}

        ModelClass = self.__class__
        table = class_mapper(ModelClass).mapped_table
        field_names = [field.name for field in table.c]

        for field_name in field_names:
            value = getattr(self, field_name, None)
            out[field_name] = value
        return out


def make_uuid():
    return str(uuid.uuid4())


def auto_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = kwargs.pop('db_session', default_db_session)

        args = args + (db_session,)
        return func(*args, **kwargs)
    return wrapper
