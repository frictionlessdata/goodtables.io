from sqlalchemy import Column, Unicode, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from goodtablesio.models.base import Base, BaseModelMixin


class Integration(Base, BaseModelMixin):

    __tablename__ = 'integrations'

    name = Column(Unicode, primary_key=True)
    description = Column(Unicode)
    active = Column(Boolean, nullable=False, default=True)

    users = relationship(
        'User', backref='integrations', cascade='all',
        secondary=Table(
            'integration_users', Base.metadata,
            Column('integration_name', Unicode,
                   ForeignKey('integrations.name', ondelete='CASCADE'),
                   primary_key=True),
            Column('user_id', Unicode,
                   ForeignKey('users.id', ondelete='CASCADE'),
                   primary_key=True),
            Column('active', Boolean, nullable=False, default=True),
            Column('conf', JSONB)))
