import logging
import datetime

from sqlalchemy import Column, Unicode, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from flask_login import UserMixin as UserLoginMixin

from goodtablesio.services import database
from goodtablesio.models.base import Base, BaseModelMixin, make_uuid
from goodtablesio.models.plan import Plan
from goodtablesio.models.subscription import Subscription


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
    conf = Column(MutableDict.as_mutable(JSONB))

    def get_id(self):
        """This method is required by Flask-Login"""
        return self.id

    subscriptions = relationship(
        'Subscription', primaryjoin='Subscription.user_id == User.id')

    @property
    def subscription(self):
        for subscription in self.subscriptions:
            if subscription.active:
                return subscription
        return None

    @property
    def plan(self):
        if self.subscription:
            return self.subscription.plan
        return None

    def set_plan(self, plan_name):

        # Finish any existing subscription
        (
            database['session'].
            query(Subscription).
            filter_by(user_id=self.id, active=True).
            update({"active": False, "finished": datetime.datetime.utcnow()})
        )

        # Create a new subscription
        plan = (
            database['session'].
            query(Plan).
            filter_by(name=plan_name).
            one_or_none()
        )

        if not plan:
            raise ValueError('Unknown plan name: {}'.format(plan_name))

        if not plan.frequency:
            expiration_timestamp = None
        elif plan.frequency == 'month':
            expiration_timestamp = (
                datetime.datetime.utcnow() + datetime.timedelta(days=30))
        elif plan.frequency == 'year':
            expiration_timestamp = (
                datetime.datetime.utcnow() + datetime.timedelta(days=365))

        sub = Subscription(
            plan_id=plan.id,
            user_id=self.id,
            active=True,
            started=datetime.datetime.utcnow(),
            expires=expiration_timestamp
        )

        database['session'].add(sub)
        database['session'].commit()

        return plan

    def extend_subscription(self, days=None):

        if not self.subscription:
            raise ValueError('User {} has no active subscription')

        if not days:
            if self.plan.frequency == 'month':
                days = 30
            elif self.plan.frequency == 'year':
                days = 365
            else:
                return None

        self.subscription.expires = (
                self.subscription.expires + datetime.timedelta(days=days))
        database['session'].add(self.subscription)
        database['session'].commit()
