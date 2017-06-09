import logging
from goodtablesio.models.source import Source
log = logging.getLogger(__name__)


# Module API

class ApiSource(Source):

    __mapper_args__ = {
        'polymorphic_identity': 'api'
    }
