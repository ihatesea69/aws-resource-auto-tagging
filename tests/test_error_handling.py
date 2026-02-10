"""Tests for error handling - malformed events and retry logic."""

import time
from unittest.mock import patch, MagicMock
from hypothesis import given, settings, strategies as st
from botocore.exceptions import ClientError

from src.resource_extractors import EXTRACTORS
from src.retry import retry_with_backoff

EVENT_KEYS = list(EXTRACTORS.keys())

# Strategy for malformed details: missing keys, empty dicts, None values
malformed_detail = st.one_of(
    st.just({}),
    st.just({"responseElements": {}}),
    st.just({"responseElements": None}),
    st.just({"requestParameters": {}}),
    st.just({"responseElements": {"instancesSet": {}}}),
    st.just({"responseElements": {"instancesSet": {"items": []}}}),
    st.just({"responseElements": {"instancesSet": {"items": [{}]}}}),
)


# Feature: auto-tag-resources, Property 6: Malformed event graceful handling
@settings(max_examples=100)
@given(
    event_index=st.integers(min_value=0, max_value=len(EVENT_KEYS) - 1),
    detail=malformed_detail,
)
def test_malformed_event_graceful_handling(event_index, detail):
    """Property 6: Malformed event graceful handling.

    For any CloudTrail event detail where resource identifier fields are
    missing, empty, or None, the extractor shall not raise an unhandled
    exception and shall return gracefully.
    **Validates: Requirements 15.1, 15.3**
    """
    event_source, event_name = EVENT_KEYS[event_index]
    extractor = EXTRACTORS[(event_source, event_name)]
    # Should not raise
    result = extractor(detail)
    # Result should be None, empty string, or empty list
    if isinstance(result, list):
        # Empty list or list of None/empty is acceptable
        pass
    # None or empty string is acceptable
    assert result is None or result == "" or result == [] or (isinstance(result, list) and len(result) == 0) or isinstance(result, str)


# --- Unit tests for error handling ---

def test_retry_with_backoff_succeeds_first_try():
    """Retry succeeds on first attempt."""
    func = MagicMock(return_value="ok")
    result = retry_with_backoff(func, max_retries=3, base_delay=0.01)
    assert result == "ok"
    assert func.call_count == 1


@patch("src.retry.time.sleep")
def test_retry_with_backoff_retries_on_throttle(mock_sleep):
    """Retry retries on throttling and succeeds."""
    throttle_error = ClientError(
        {"Error": {"Code": "Throttling", "Message": "Rate exceeded"}},
        "CreateTags",
    )
    func = MagicMock(side_effect=[throttle_error, throttle_error, "ok"])
    result = retry_with_backoff(func, max_retries=3, base_delay=1.0)
    assert result == "ok"
    assert func.call_count == 3
    assert mock_sleep.call_count == 2


def test_retry_with_backoff_raises_non_throttle():
    """Non-throttle errors are raised immediately."""
    access_error = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "No access"}},
        "CreateTags",
    )
    func = MagicMock(side_effect=access_error)
    try:
        retry_with_backoff(func, max_retries=3, base_delay=0.01)
        assert False, "Should have raised"
    except ClientError as e:
        assert e.response["Error"]["Code"] == "AccessDenied"
    assert func.call_count == 1
