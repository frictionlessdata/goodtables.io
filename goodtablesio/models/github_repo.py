import logging
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, Unicode, DateTime, Boolean
from goodtablesio.models.base import Base, BaseModelMixin
log = logging.getLogger(__name__)
now = datetime.datetime.utcnow


# Module API

class GithubRepo(Base, BaseModelMixin):

    # Public

    __tablename__ = 'github_repos'

    id = Column(Unicode, primary_key=True)
    owner = Column(Unicode, nullable=False)
    repo = Column(Unicode, nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    updated = Column(DateTime(timezone=True), nullable=False, default=now)
    users = relationship('User', secondary=Table('users_github_repos', Base.metadata,
        Column('user_id', Unicode, ForeignKey('users.id')),
        Column('github_repo_id', Unicode, ForeignKey('github_repos.id')),
    ))

    @property
    def url(self):
        template = 'https://github.com/{owner}/{repo}'
        return template.format(owner=self.owner, repo=self.repo)
