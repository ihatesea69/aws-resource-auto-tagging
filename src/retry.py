"""Retry logic with exponential backoff for throttled AWS API calls."""

import time
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

THROTTLE_ERROR_CODES = {"Throttling", "ThrottlingException", "RequestLimitExceeded"}


def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """Call func(), retrying on throttling errors with exponential backoff.

    Args:
        func: A callable that makes an AWS API call.
        max_retries: Maximum number of retry attempts (default 3).
        base_delay: Base delay in seconds (doubles each retry: 1s, 2s, 4s).

    Returns:
        The return value of func() on success.

    Raises:
        ClientError: If a non-throttling error occurs, or all retries are exhausted.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code not in THROTTLE_ERROR_CODES:
                raise
            last_error = e
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                logger.warning(
                    "Throttled (attempt %d/%d), retrying in %.1fs: %s",
                    attempt + 1, max_retries, delay, error_code,
                )
                time.sleep(delay)
            else:
                logger.error(
                    "All %d retries exhausted for throttling error: %s",
                    max_retries, error_code,
                )
    raise last_error
