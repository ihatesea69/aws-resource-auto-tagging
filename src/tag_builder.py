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
        environment: Environment name from CloudFormation parameter.
        project: Project name from CloudFormation parameter.

    Returns:
        A dict with the six standard tag keys.
    """
    return {
        "Owner": owner,
        "CreatedBy": arn,
        "CreationDate": event_time,
        "Environment": environment,
        "Project": project,
        "AutoTagged": "true",
    }
