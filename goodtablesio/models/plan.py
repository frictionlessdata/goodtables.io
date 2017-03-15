import logging
import datetime

from sqlalchemy import (
    Column, Unicode, DateTime, Boolean, Integer, Enum)

from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


log = logging.getLogger(__name__)


class Plan(Base, BaseModelMixin):

    __tablename__ = 'plans'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode, nullable=False, unique=True)
    description = Column(Unicode, unique=True)
    active = Column(Boolean, default=True)
    price = Column(Integer)
    frequency = Column(Enum('', 'month', 'year'))
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
