import logging
import datetime
from sqlalchemy import Column, Unicode, DateTime, ForeignKey
from goodtablesio.models.base import Base, BaseModelMixin, make_uuid, make_token
log = logging.getLogger(__name__)


# Helpers


# Module API

class ApiToken(Base, BaseModelMixin):

    __tablename__ = 'api_tokens'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    user_id = Column(Unicode, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(Unicode, nullable=False, unique=True, default=make_token)
    description = Column(Unicode, nullable=True)
    created = Column(DateTime(timezone=True),
        nullable=False, default=datetime.datetime.utcnow)
