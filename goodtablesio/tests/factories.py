import uuid
import datetime

import factory

from goodtablesio import services
from goodtablesio.models.job import Job


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
        sqlalchemy_session = services.db_session

    id = factory.Sequence(lambda n: str(uuid.uuid4()))
    created = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    plugin_name = 'api'
    status = 'created'
