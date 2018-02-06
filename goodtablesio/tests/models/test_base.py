import uuid

from goodtablesio.models.base import make_uuid


def test_make_uuid():
    assert uuid.UUID(make_uuid(), version=1)
