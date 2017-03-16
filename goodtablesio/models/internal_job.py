import logging
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Unicode, DateTime,  ForeignKey
from goodtablesio.models.base import Base, BaseModelMixin, make_uuid
log = logging.getLogger(__name__)


class InternalJob(Base, BaseModelMixin):

    __tablename__ = 'internal_jobs'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode, nullable=False)
    conf = Column(JSONB, default={}, nullable=False)
    status = Column(Unicode, default='created', nullable=False)
    created = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)
    finished = Column(DateTime(timezone=True))
    error = Column(JSONB)
    user_id = Column(Unicode, ForeignKey('users.id'))
    user = relationship('User', backref='tasks')
