"""Build the standard tag set applied to every auto-tagged resource."""


def build_tags(
    owner: str,
    arn: str,
    event_time: str,
    environment: str,
    project: str,
) -> dict:
    """Build the standard tag payload.

    Args:
        owner: The extracted owner name (from extract_owner).
        arn: The full ARN from the userIdentity field.
        event_time: The event time in ISO 8601 format.
        environment: Environment name (unused, kept for interface compatibility).
        project: Project name (unused, kept for interface compatibility).

    Returns:
        A dict with the three standard tag keys.
    """
    return {
        "Owner": owner,
        "CreatedBy": arn,
        "CreationDate": event_time,
    }
