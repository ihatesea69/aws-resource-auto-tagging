"""Shared error handling for service handlers."""

import logging
import functools
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

PERMISSIONS_ERROR_CODES = {"AccessDeniedException", "UnauthorizedAccess", "AccessDenied"}


def handle_tagging_errors(event_name):
    """Decorator that wraps a service handler with standard error handling.

    Catches:
    - Missing resource IDs (already handled by each handler returning early)
    - Permissions errors -> logs specific insufficient-permissions message
    - General ClientError -> logs error code, message, resource ID, event name
    - Unexpected exceptions -> logs and returns without raising
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(detail, tags):
            try:
                return func(detail, tags)
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "")
                error_msg = e.response.get("Error", {}).get("Message", "")
                if error_code in PERMISSIONS_ERROR_CODES:
                    logger.error(
                        "Insufficient permissions to tag resource for event %s: %s - %s",
                        event_name, error_code, error_msg,
                    )
                else:
                    logger.error(
                        "Error tagging resource for event %s: code=%s, message=%s",
                        event_name, error_code, error_msg,
                    )
            except Exception as e:
                logger.error(
                    "Unexpected error in handler for event %s: %s",
                    event_name, str(e), exc_info=True,
                )
        return wrapper
    return decorator
