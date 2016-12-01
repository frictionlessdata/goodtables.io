import uuid
import datetime

from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import JSONB
import factory

from goodtablesio import services
from goodtablesio.models import Job


# TODO: Use SQLAlchemy models when we have a proper ORM

class Job(factory.Factory):

    class Meta:
        model = Job

    job_id = factory.Sequence(lambda n: str(uuid.uuid4()))
    created = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    plugin_name = 'api'
    plugin_conf = None
    status = 'created'
    finished = None
    report = None
    error = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        row = {}
        for field in ('job_id', 'plugin_name', 'plugin_conf',
                      'created', 'finished', 'report', 'status', 'error'):
            row[field] = kwargs.get(field)

        services.database['jobs'].insert(row,
                                         types={'created': DateTime,
                                                'finished': DateTime,
                                                'report': JSONB,
                                                'error': JSONB,
                                                'plugin_conf': JSONB},
                                         ensure=True)

        return model_class(*args, **kwargs)
