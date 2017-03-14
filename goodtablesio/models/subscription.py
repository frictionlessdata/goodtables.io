import logging
import datetime

from sqlalchemy import (
    Column, Unicode, DateTime, Boolean, ForeignKey)
from sqlalchemy.orm import relationship

from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


log = logging.getLogger(__name__)


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
