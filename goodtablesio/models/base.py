import hmac
import uuid
import hashlib

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


def make_token():
    # https://stackoverflow.com/questions/17823566/creating-api-tokens-for-third-parties
    token = hmac.new(make_uuid().encode('utf-8'), digestmod=hashlib.sha1)
    token = token.hexdigest().upper()
    return token
