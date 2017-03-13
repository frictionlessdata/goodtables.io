import logging
import datetime

from sqlalchemy import (
    Column, Unicode, DateTime, Boolean, Integer, ForeignKey, Enum)
from sqlalchemy.orm import relationship

from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


log = logging.getLogger(__name__)


class Plan(Base, BaseModelMixin):

    __tablename__ = 'plans'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode, nullable=False, unique=True)
    description = Column(Unicode, unique=True, nullable=True)
    active = Column(Boolean, default=True)
    price = Column(Integer)
    frequency = Column(Enum('', 'month', 'year'))
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class Subscription(Base, BaseModelMixin):

    __tablename__ = 'subscriptions'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    plan_id = Column(Unicode, ForeignKey('plans.id'))
    user_id = Column(Unicode, ForeignKey('users.id'))

    active = Column(Boolean, default=True)
    started = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    expires = Column(DateTime(timezone=True))
    finished = Column(DateTime(timezone=True))

    plan = relationship(
        'Plan', primaryjoin='Subscription.plan_id == Plan.id')
