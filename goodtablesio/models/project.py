import datetime

from sqlalchemy import (
    Column, Unicode, DateTime, Boolean, ForeignKey, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from goodtablesio.models.base import Base, BaseModelMixin, make_uuid


class Project(Base, BaseModelMixin):

    __tablename__ = 'projects'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode)
    active = Column(Boolean, nullable=False, default=False)
    updated = Column(DateTime(timezone=True), nullable=False,
                     default=datetime.datetime.utcnow)
    conf = Column(JSONB)
    integration_name = Column(Unicode, ForeignKey('integrations.name'))
    integration = relationship(
        'Integration',
        primaryjoin='Project.integration_name == Integration.name')

    users = relationship(
        'User', backref='projects', cascade='all',
        secondary=Table(
            'project_users', Base.metadata,
            Column('project_id', Unicode,
                   ForeignKey('projects.id', ondelete='CASCADE'),
                   primary_key=True),
            Column('user_id', Unicode,
                   ForeignKey('users.id', ondelete='CASCADE'),
                   primary_key=True),
            Column('role', Unicode, nullable=False, default='default')))

    __mapper_args__ = {
        'polymorphic_on': integration_name,
        'polymorphic_identity': 'project'
    }
