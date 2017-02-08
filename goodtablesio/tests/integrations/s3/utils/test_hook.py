from goodtablesio.tests.integrations.s3 import mock_responses
from goodtablesio.integrations.s3.utils.hook import (
    get_bucket_from_hook_payload)


def test_get_bucket_from_hook_payload():

    payload = mock_responses.s3_notification_event

    assert get_bucket_from_hook_payload(payload) == 'test-gtio-1'


def test_get_bucket_from_hook_wrong_payload():

    payloads = [
        {'a': 'b'},
        {'Records': 'a'},
        'a',
        None
    ]

    for payload in payloads:
        assert get_bucket_from_hook_payload(payload) is None
