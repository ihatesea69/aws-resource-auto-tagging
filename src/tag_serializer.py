"""Tag serialization/deserialization for AWS service-specific tagging APIs.

All services use the same wire format [{"Key": k, "Value": v}, ...] but are
kept as separate function pairs for clarity and future divergence.
"""


def serialize_ec2_tags(tags: dict) -> list:
    """Convert internal tag dict to EC2 CreateTags format."""
    return [{"Key": k, "Value": v} for k, v in tags.items()]


def deserialize_ec2_tags(tag_list: list) -> dict:
    """Convert EC2 tag list back to internal dict."""
    return {item["Key"]: item["Value"] for item in tag_list}


def serialize_s3_tags(tags: dict) -> list:
    """Convert internal tag dict to S3 PutBucketTagging TagSet format."""
    return [{"Key": k, "Value": v} for k, v in tags.items()]


def deserialize_s3_tags(tag_list: list) -> dict:
    """Convert S3 TagSet list back to internal dict."""
    return {item["Key"]: item["Value"] for item in tag_list}


def serialize_arn_tags(tags: dict) -> list:
    """Convert internal tag dict to ARN-based service tag format.

    Used by RDS, DynamoDB, Lambda, ELB, EFS, SNS, SQS,
    Secrets Manager, OpenSearch, ECS, Step Functions.
    """
    return [{"Key": k, "Value": v} for k, v in tags.items()]


def deserialize_arn_tags(tag_list: list) -> dict:
    """Convert ARN-based service tag list back to internal dict."""
    return {item["Key"]: item["Value"] for item in tag_list}
