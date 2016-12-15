import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


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
