"""AutoTag Lambda - Automatically tags newly created AWS resources with creator identity."""

import json
import os
import logging

from src.identity import extract_owner
from src.tag_builder import build_tags
from src.tag_printer import print_tags
from src.config import SERVICE_HANDLERS

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "Development")
PROJECT = os.environ.get("PROJECT", "CostTracking")


def lambda_handler(event, context):
    """Entry point for the AutoTag Lambda function.

    Receives CloudTrail events via EventBridge, extracts creator identity,
    builds standard tags, and dispatches to the appropriate service handler.
    """
    logger.info("Event received: %s", json.dumps(event))

    try:
        detail = event.get("detail", {})
        event_source = detail.get("eventSource", "")
        event_name = detail.get("eventName", "")

        logger.info("Processing event: %s / %s", event_source, event_name)

        # Extract creator identity
        user_identity = detail.get("userIdentity", {})
        owner = extract_owner(user_identity)
        arn = user_identity.get("arn", "Unknown") if user_identity else "Unknown"
        event_time = detail.get("eventTime", "")

        # Build standard tag set
        tags = build_tags(owner, arn, event_time, ENVIRONMENT, PROJECT)

        # Log tags
        logger.info("Tags to apply: %s", print_tags(tags))

        # Look up and dispatch to service handler
        handler = SERVICE_HANDLERS.get((event_source, event_name))
        if handler is None:
            logger.warning("No handler for event: %s / %s", event_source, event_name)
            return {"statusCode": 200, "body": "No handler for event"}

        handler(detail, tags)

        return {"statusCode": 200, "body": "Event processed"}

    except Exception as e:
        logger.error("Unexpected error processing event: %s", str(e), exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": type(e).__name__,
                "message": str(e),
                "eventName": event.get("detail", {}).get("eventName", ""),
            }),
        }
