import uuid
import datetime

import factory
from faker import Faker

from goodtablesio.models.job import Job
from goodtablesio.models.user import User
from goodtablesio.models.plan import Plan
from goodtablesio.models.source import Source
from goodtablesio.models.integration import Integration
from goodtablesio.services import database
from goodtablesio.integrations.github.models.repo import GithubRepo
from goodtablesio.integrations.s3.models.bucket import S3Bucket


fake = Faker()


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


class Integration(FactoryBase):

    class Meta:
        model = Integration
        sqlalchemy_session = database['session']

    name = factory.Faker('name')


class Source(FactoryBase):

    class Meta:
        model = Source
        sqlalchemy_session = database['session']
        exclude = ('integration',)

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    name = factory.Faker('name')
    updated = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    active = True

    @property
    def integration(self):
        return database['session'].query(Integration).get('api')


class GithubRepo(FactoryBase):

    class Meta:
        model = GithubRepo
        sqlalchemy_session = database['session']
        exclude = ('url', 'owner', 'repo', 'integration',)

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    name = factory.LazyAttribute(lambda a: '{0}/{1}'.format(fake.user_name(),
                                                            fake.user_name()))
    updated = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    active = True

    @property
    def integration(self):
        return database['session'].query(Integration).get('github')

    @property
    def url(self):

        parts = self.name.split('/')

        template = 'https://github.com/{owner}/{repo}'
        return template.format(owner=parts[0], repo=parts[1])

    @property
    def owner(self):

        parts = self.name.split('/')

        return parts[0]

    @property
    def repo(self):

        parts = self.name.split('/')

        return parts[1]


class S3Bucket(FactoryBase):

    class Meta:
        model = S3Bucket
        sqlalchemy_session = database['session']
        exclude = ('integration',)

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    name = factory.Faker('user_name')
    updated = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    active = True

    @property
    def integration(self):
        return database['session'].query(Integration).get('s3')


class Plan(FactoryBase):

    class Meta:
        model = Plan
        sqlalchemy_session = database['session']

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    name = 'paid'
    description = ''
    active = True
    frequency = 'month'
    price = 1000
    created = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
