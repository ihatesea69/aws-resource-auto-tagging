"""Handlers for DynamoDB, Lambda, ELB, EFS, SNS, SQS, Secrets Manager,
OpenSearch, ECS, and Step Functions auto-tagging."""

import logging
import boto3
try:
    from tag_serializer import serialize_arn_tags
    from error_handler import handle_tagging_errors
except ImportError:
    from src.tag_serializer import serialize_arn_tags
    from src.error_handler import handle_tagging_errors

logger = logging.getLogger(__name__)


def _client(service, detail):
    region = detail.get("awsRegion")
    return boto3.client(service, region_name=region) if region else boto3.client(service)


@handle_tagging_errors("CreateTable")
def handle_dynamodb_create_table(detail, tags):
    table_arn = detail.get("responseElements", {}).get("tableDescription", {}).get("tableArn")
    if not table_arn:
        logger.warning("No tableArn found in CreateTable event")
        return
    client = _client("dynamodb", detail)
    client.tag_resource(ResourceArn=table_arn, Tags=serialize_arn_tags(tags))
    logger.info("Tagged DynamoDB table: %s", table_arn)


@handle_tagging_errors("CreateFunction20150331")
def handle_lambda_create_function(detail, tags):
    func_arn = detail.get("responseElements", {}).get("functionArn")
    if not func_arn:
        logger.warning("No functionArn found in CreateFunction event")
        return
    client = _client("lambda", detail)
    client.tag_resource(Resource=func_arn, Tags={t["Key"]: t["Value"] for t in serialize_arn_tags(tags)})
    logger.info("Tagged Lambda function: %s", func_arn)


@handle_tagging_errors("CreateLoadBalancer")
def handle_elb_create_load_balancer(detail, tags):
    lbs = detail.get("responseElements", {}).get("loadBalancers", [])
    lb_arn = lbs[0].get("loadBalancerArn") if lbs else None
    if not lb_arn:
        logger.warning("No loadBalancerArn found in CreateLoadBalancer event")
        return
    client = _client("elbv2", detail)
    client.add_tags(ResourceArns=[lb_arn], Tags=serialize_arn_tags(tags))
    logger.info("Tagged load balancer: %s", lb_arn)


@handle_tagging_errors("CreateTargetGroup")
def handle_elb_create_target_group(detail, tags):
    tgs = detail.get("responseElements", {}).get("targetGroups", [])
    tg_arn = tgs[0].get("targetGroupArn") if tgs else None
    if not tg_arn:
        logger.warning("No targetGroupArn found in CreateTargetGroup event")
        return
    client = _client("elbv2", detail)
    client.add_tags(ResourceArns=[tg_arn], Tags=serialize_arn_tags(tags))
    logger.info("Tagged target group: %s", tg_arn)


@handle_tagging_errors("CreateFileSystem")
def handle_efs_create_file_system(detail, tags):
    fs_id = detail.get("responseElements", {}).get("fileSystemId")
    if not fs_id:
        logger.warning("No fileSystemId found in CreateFileSystem event")
        return
    client = _client("efs", detail)
    client.tag_resource(ResourceId=fs_id, Tags=serialize_arn_tags(tags))
    logger.info("Tagged EFS file system: %s", fs_id)


@handle_tagging_errors("CreateTopic")
def handle_sns_create_topic(detail, tags):
    topic_arn = detail.get("responseElements", {}).get("topicArn")
    if not topic_arn:
        logger.warning("No topicArn found in CreateTopic event")
        return
    client = _client("sns", detail)
    client.tag_resource(ResourceArn=topic_arn, Tags=serialize_arn_tags(tags))
    logger.info("Tagged SNS topic: %s", topic_arn)


@handle_tagging_errors("CreateQueue")
def handle_sqs_create_queue(detail, tags):
    queue_url = detail.get("responseElements", {}).get("queueUrl")
    if not queue_url:
        logger.warning("No queueUrl found in CreateQueue event")
        return
    client = _client("sqs", detail)
    client.tag_queue(QueueUrl=queue_url, Tags={t["Key"]: t["Value"] for t in serialize_arn_tags(tags)})
    logger.info("Tagged SQS queue: %s", queue_url)


@handle_tagging_errors("CreateSecret")
def handle_secretsmanager_create_secret(detail, tags):
    secret_arn = detail.get("responseElements", {}).get("aRN")
    if not secret_arn:
        logger.warning("No ARN found in CreateSecret event")
        return
    client = _client("secretsmanager", detail)
    client.tag_resource(SecretId=secret_arn, Tags=serialize_arn_tags(tags))
    logger.info("Tagged secret: %s", secret_arn)


@handle_tagging_errors("CreateDomain")
def handle_opensearch_create_domain(detail, tags):
    domain_arn = detail.get("responseElements", {}).get("domainStatus", {}).get("aRN")
    if not domain_arn:
        logger.warning("No ARN found in CreateDomain event")
        return
    client = _client("opensearch", detail)
    client.add_tags(ARN=domain_arn, TagList=serialize_arn_tags(tags))
    logger.info("Tagged OpenSearch domain: %s", domain_arn)


@handle_tagging_errors("CreateCluster")
def handle_ecs_create_cluster(detail, tags):
    cluster_arn = detail.get("responseElements", {}).get("cluster", {}).get("clusterArn")
    if not cluster_arn:
        logger.warning("No clusterArn found in CreateCluster event")
        return
    client = _client("ecs", detail)
    client.tag_resource(resourceArn=cluster_arn, tags=serialize_arn_tags(tags))
    logger.info("Tagged ECS cluster: %s", cluster_arn)


@handle_tagging_errors("CreateStateMachine")
def handle_stepfunctions_create_state_machine(detail, tags):
    sm_arn = detail.get("responseElements", {}).get("stateMachineArn")
    if not sm_arn:
        logger.warning("No stateMachineArn found in CreateStateMachine event")
        return
    client = _client("stepfunctions", detail)
    client.tag_resource(resourceArn=sm_arn, tags=serialize_arn_tags(tags))
    logger.info("Tagged state machine: %s", sm_arn)
