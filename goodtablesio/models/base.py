import hmac
import uuid
import hashlib
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from goodtablesio.services import database
Base = declarative_base()


# Module API

class BaseModelMixin(object):

    # Public

    @classmethod
    def create(cls, **params):
        instance = cls(**params)
        database['session'].add(instance)
        database['session'].commit()
        return instance

    @classmethod
    def query(cls):
        return database['session'].query(cls)

    @classmethod
    def get(cls, id):
        return database['session'].query(cls).get(id)

    def to_dict(self):
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


def make_token():
    # https://stackoverflow.com/questions/17823566/creating-api-tokens-for-third-parties
    token = hmac.new(make_uuid().encode('utf-8'), digestmod=hashlib.sha1)
    token = token.hexdigest().upper()
    return token
