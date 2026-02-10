"""Identity extraction from CloudTrail userIdentity fields."""


def extract_owner(user_identity: dict) -> str:
    """Extract the owner name from a CloudTrail userIdentity dict.

    Args:
        user_identity: The userIdentity dict from a CloudTrail event detail.

    Returns:
        The owner name string based on identity type:
        - IAMUser -> userName
        - AssumedRole -> session name (last segment of ARN after '/')
        - Root -> "root"
        - FederatedUser -> userName
        - Unknown/missing -> "Unknown"
    """
    if not user_identity or not isinstance(user_identity, dict):
        return "Unknown"

    identity_type = user_identity.get("type", "")

    if identity_type == "IAMUser":
        return user_identity.get("userName", "Unknown")

    if identity_type == "AssumedRole":
        arn = user_identity.get("arn", "")
        if arn and "/" in arn:
            return arn.rsplit("/", 1)[-1]
        return "Unknown"

    if identity_type == "Root":
        return "root"

    if identity_type == "FederatedUser":
        return user_identity.get("userName", "Unknown")

    return "Unknown"
