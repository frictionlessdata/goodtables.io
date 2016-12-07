import uuid
import datetime

import factory

from goodtablesio import services
from goodtablesio.models import Job


class Job(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Job
        sqlalchemy_session = services.db_session
        force_flush = True

    job_id = factory.Sequence(lambda n: str(uuid.uuid4()))
    created = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    plugin_name = 'api'
    status = 'created'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        out = super()._create(model_class, *args, **kwargs)

        # Actually store the object on the DB
        cls._meta.sqlalchemy_session.commit()

        return out
