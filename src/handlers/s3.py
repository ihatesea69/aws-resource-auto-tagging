"""S3 service handler for auto-tagging."""

import logging
import boto3
from botocore.exceptions import ClientError
try:
    from tag_serializer import serialize_s3_tags, deserialize_s3_tags
    from error_handler import handle_tagging_errors
except ImportError:
    from src.tag_serializer import serialize_s3_tags, deserialize_s3_tags
    from src.error_handler import handle_tagging_errors

logger = logging.getLogger(__name__)


@handle_tagging_errors("CreateBucket")
def handle_s3_create_bucket(detail, tags):
    """Tag a new S3 bucket, merging with any existing tags."""
    bucket_name = detail.get("requestParameters", {}).get("bucketName")
    if not bucket_name:
        logger.warning("No bucketName found in CreateBucket event")
        return

    s3 = boto3.client("s3")

    existing_tags = {}
    try:
        response = s3.get_bucket_tagging(Bucket=bucket_name)
        existing_tags = deserialize_s3_tags(response.get("TagSet", []))
    except ClientError:
        pass  # No existing tags

    merged = {**existing_tags, **tags}
    s3.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={"TagSet": serialize_s3_tags(merged)},
    )
    logger.info("Tagged S3 bucket: %s", bucket_name)
