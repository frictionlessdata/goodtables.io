import datetime

from sqlalchemy import (
    Column, Unicode, Integer, DateTime, Boolean, ForeignKey, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


class Source(Base, BaseModelMixin):

    __tablename__ = 'sources'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode)
    active = Column(Boolean, nullable=False, default=False)
    updated = Column(DateTime(timezone=True), nullable=False,
                     default=datetime.datetime.utcnow)
    job_number = Column(Integer)
    conf = Column(JSONB)
    integration_name = Column(Unicode, ForeignKey('integrations.name'))
    integration = relationship(
        'Integration',
        primaryjoin='Source.integration_name == Integration.name')

    users = relationship('User', backref='sources', secondary=Table(
            'source_users', Base.metadata,
            Column('source_id', Unicode,
                   ForeignKey('sources.id', ondelete='CASCADE'),
                   primary_key=True),
            Column('user_id', Unicode,
                   ForeignKey('users.id', ondelete='CASCADE'),
                   primary_key=True),
            Column('role', Unicode, nullable=False, default='default')))

    jobs = relationship(
        'Job', backref='source', primaryjoin='Job.source_id == Source.id',
        order_by='Job.created')

    __mapper_args__ = {
        'polymorphic_on': integration_name,
        'polymorphic_identity': 'source'
    }

    def to_api(self, with_last_job=False):
        source = {
            'id': self.id,
            'name': self.name,
            'integration_name': self.integration_name,
            'active': self.active,
        }
        if with_last_job:
            source['last_job'] = (self.last_job.to_api()
                                  if self.last_job else None)

        return source

    @property
    def last_job(self):
        return self.jobs[-1] if self.jobs else None
