"""Human-readable tag printing and parsing for logging/debugging."""


def print_tags(tags: dict) -> str:
    """Format a tag dict as a human-readable string.

    Example: {"Owner": "alice", "AutoTagged": "true"} -> "Owner=alice, AutoTagged=true"
    """
    return ", ".join(f"{k}={v}" for k, v in tags.items())


def parse_tags(tag_string: str) -> dict:
    """Parse a printed tag string back into a dict.

    Example: "Owner=alice, AutoTagged=true" -> {"Owner": "alice", "AutoTagged": "true"}
    """
    if not tag_string or not tag_string.strip():
        return {}
    result = {}
    for pair in tag_string.split(", "):
        key, _, value = pair.partition("=")
        result[key] = value
    return result
