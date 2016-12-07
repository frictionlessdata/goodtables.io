import datetime
import uuid

from sqlalchemy import Column, Unicode, DateTime
from sqlalchemy.orm import class_mapper
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def _make_uuid():
    return str(uuid.uuid4())


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


class Job(Base, BaseModelMixin):

    __tablename__ = 'jobs'

    job_id = Column(Unicode, primary_key=True, default=_make_uuid)
    status = Column(Unicode, default='created')
    plugin_name = Column(Unicode, default='api')
    plugin_conf = Column(JSONB)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    finished = Column(DateTime)
    report = Column(JSONB)
    error = Column(JSONB)
