import uuid
import datetime

import factory

from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.services import database
from goodtablesio.integrations.github.models.repo import GithubRepo


class FactoryBase(factory.alchemy.SQLAlchemyModelFactory):
    """
    Base class to be applied to all factories
    """

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Note: Factories are meant to create the object and just store it into
            the Session, not the actual DB. In our case, there are situations
            where we actually require the object to be stored in the DB ( eg
            when using tasks, as they use a different session, or when testing
            getting things from then DB) so you can pass a `_save_in_db`
            keyword to force it.
        """

        _save_in_db = kwargs.pop('_save_in_db', False)
        out = super()._create(model_class, *args, **kwargs)
        if _save_in_db:

            # Actually store the object on the DB
            cls._meta.sqlalchemy_session.commit()

        return out


class Job(FactoryBase):

    class Meta:
        model = Job
        sqlalchemy_session = database['session']

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    created = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    integration_name = 'api'
    status = 'created'


class User(FactoryBase):

    class Meta:
        model = User
        sqlalchemy_session = database['session']

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    name = factory.Faker('user_name')
    display_name = factory.Faker('name')
    email = factory.Faker('email')
    created = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    admin = False


class GithubRepo(FactoryBase):

    class Meta:
        model = GithubRepo
        sqlalchemy_session = database['session']

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    owner = factory.Faker('name')
    repo = factory.Faker('name')
    updated = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    active = True
