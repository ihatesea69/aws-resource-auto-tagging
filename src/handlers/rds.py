"""RDS service handlers for auto-tagging."""

import logging
import boto3
from src.tag_serializer import serialize_arn_tags
from src.error_handler import handle_tagging_errors

logger = logging.getLogger(__name__)


@handle_tagging_errors("CreateDBInstance")
def handle_rds_create_db_instance(detail, tags):
    db_arn = detail.get("responseElements", {}).get("dBInstanceArn")
    if not db_arn:
        logger.warning("No dBInstanceArn found in CreateDBInstance event")
        return
    region = detail.get("awsRegion")
    rds = boto3.client("rds", region_name=region) if region else boto3.client("rds")
    rds.add_tags_to_resource(ResourceName=db_arn, Tags=serialize_arn_tags(tags))
    logger.info("Tagged RDS instance: %s", db_arn)


@handle_tagging_errors("CreateDBCluster")
def handle_rds_create_db_cluster(detail, tags):
    cluster_arn = detail.get("responseElements", {}).get("dBClusterArn")
    if not cluster_arn:
        logger.warning("No dBClusterArn found in CreateDBCluster event")
        return
    region = detail.get("awsRegion")
    rds = boto3.client("rds", region_name=region) if region else boto3.client("rds")
    rds.add_tags_to_resource(ResourceName=cluster_arn, Tags=serialize_arn_tags(tags))
    logger.info("Tagged RDS cluster: %s", cluster_arn)
