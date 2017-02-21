import logging
import datetime

from sqlalchemy import Column, Unicode, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from flask_login import UserMixin as UserLoginMixin

from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


log = logging.getLogger(__name__)


class User(Base, BaseModelMixin, UserLoginMixin):

    __tablename__ = 'users'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode, unique=True, nullable=False)
    email = Column(Unicode, unique=True, nullable=True)
    display_name = Column(Unicode)
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    admin = Column(Boolean, nullable=False, default=False)
    provider_ids = Column(MutableDict.as_mutable(JSONB))
    conf = Column(JSONB)

    def get_id(self):
        """This method is required by Flask-Login"""
        return self.id
