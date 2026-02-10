"""Pure resource ID extraction functions for each supported event.

These functions extract resource identifiers from CloudTrail event details
without making any AWS API calls, making them testable in isolation.
"""


def _safe_get(d, *keys):
    """Safely traverse nested dicts, returning None if any key is missing or value is None."""
    current = d
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
        if current is None:
            return None
    return current


def extract_ec2_run_instances_ids(detail):
    """Extract instance IDs and volume IDs from RunInstances."""
    items = _safe_get(detail, "responseElements", "instancesSet", "items")
    if not isinstance(items, list):
        return []
    ids = []
    for item in items:
        if not isinstance(item, dict):
            continue
        iid = item.get("instanceId")
        if iid:
            ids.append(iid)
        bd_items = _safe_get(item, "blockDeviceMapping", "items")
        if isinstance(bd_items, list):
            for bd in bd_items:
                if isinstance(bd, dict):
                    vid = _safe_get(bd, "ebs", "volumeId")
                    if vid:
                        ids.append(vid)
    return ids


def extract_ec2_create_security_group_id(detail):
    return _safe_get(detail, "responseElements", "groupId")


def extract_ec2_create_image_id(detail):
    return _safe_get(detail, "responseElements", "imageId")


def extract_ec2_create_volume_id(detail):
    return _safe_get(detail, "responseElements", "volumeId")


def extract_ec2_create_snapshot_id(detail):
    return _safe_get(detail, "responseElements", "snapshotId")


def extract_ec2_allocate_address_id(detail):
    return _safe_get(detail, "responseElements", "allocationId")


def extract_ec2_create_network_interface_id(detail):
    return _safe_get(detail, "responseElements", "networkInterface", "networkInterfaceId")


def extract_ec2_create_vpc_id(detail):
    return _safe_get(detail, "responseElements", "vpc", "vpcId")


def extract_ec2_create_subnet_id(detail):
    return _safe_get(detail, "responseElements", "subnet", "subnetId")


def extract_ec2_create_internet_gateway_id(detail):
    return _safe_get(detail, "responseElements", "internetGateway", "internetGatewayId")


def extract_ec2_create_nat_gateway_id(detail):
    return _safe_get(detail, "responseElements", "natGateway", "natGatewayId")


def extract_s3_create_bucket_name(detail):
    return _safe_get(detail, "requestParameters", "bucketName")


def extract_rds_create_db_instance_arn(detail):
    return _safe_get(detail, "responseElements", "dBInstanceArn")


def extract_rds_create_db_cluster_arn(detail):
    return _safe_get(detail, "responseElements", "dBClusterArn")


def extract_dynamodb_create_table_arn(detail):
    return _safe_get(detail, "responseElements", "tableDescription", "tableArn")


def extract_lambda_create_function_arn(detail):
    return _safe_get(detail, "responseElements", "functionArn")


def extract_elb_create_load_balancer_arn(detail):
    lbs = _safe_get(detail, "responseElements", "loadBalancers")
    if not isinstance(lbs, list) or not lbs:
        return None
    return lbs[0].get("loadBalancerArn") if isinstance(lbs[0], dict) else None


def extract_elb_create_target_group_arn(detail):
    tgs = _safe_get(detail, "responseElements", "targetGroups")
    if not isinstance(tgs, list) or not tgs:
        return None
    return tgs[0].get("targetGroupArn") if isinstance(tgs[0], dict) else None


def extract_efs_create_file_system_id(detail):
    return _safe_get(detail, "responseElements", "fileSystemId")


def extract_sns_create_topic_arn(detail):
    return _safe_get(detail, "responseElements", "topicArn")


def extract_sqs_create_queue_url(detail):
    return _safe_get(detail, "responseElements", "queueUrl")


def extract_secretsmanager_create_secret_arn(detail):
    return _safe_get(detail, "responseElements", "aRN")


def extract_opensearch_create_domain_arn(detail):
    return _safe_get(detail, "responseElements", "domainStatus", "aRN")


def extract_ecs_create_cluster_arn(detail):
    return _safe_get(detail, "responseElements", "cluster", "clusterArn")


def extract_stepfunctions_create_state_machine_arn(detail):
    return _safe_get(detail, "responseElements", "stateMachineArn")


# Map of (eventSource, eventName) -> extractor function
EXTRACTORS = {
    ("ec2.amazonaws.com", "RunInstances"): extract_ec2_run_instances_ids,
    ("ec2.amazonaws.com", "CreateSecurityGroup"): extract_ec2_create_security_group_id,
    ("ec2.amazonaws.com", "CreateImage"): extract_ec2_create_image_id,
    ("ec2.amazonaws.com", "CreateVolume"): extract_ec2_create_volume_id,
    ("ec2.amazonaws.com", "CreateSnapshot"): extract_ec2_create_snapshot_id,
    ("ec2.amazonaws.com", "AllocateAddress"): extract_ec2_allocate_address_id,
    ("ec2.amazonaws.com", "CreateNetworkInterface"): extract_ec2_create_network_interface_id,
    ("ec2.amazonaws.com", "CreateVpc"): extract_ec2_create_vpc_id,
    ("ec2.amazonaws.com", "CreateSubnet"): extract_ec2_create_subnet_id,
    ("ec2.amazonaws.com", "CreateInternetGateway"): extract_ec2_create_internet_gateway_id,
    ("ec2.amazonaws.com", "CreateNatGateway"): extract_ec2_create_nat_gateway_id,
    ("s3.amazonaws.com", "CreateBucket"): extract_s3_create_bucket_name,
    ("rds.amazonaws.com", "CreateDBInstance"): extract_rds_create_db_instance_arn,
    ("rds.amazonaws.com", "CreateDBCluster"): extract_rds_create_db_cluster_arn,
    ("dynamodb.amazonaws.com", "CreateTable"): extract_dynamodb_create_table_arn,
    ("lambda.amazonaws.com", "CreateFunction20150331"): extract_lambda_create_function_arn,
    ("elasticloadbalancing.amazonaws.com", "CreateLoadBalancer"): extract_elb_create_load_balancer_arn,
    ("elasticloadbalancing.amazonaws.com", "CreateTargetGroup"): extract_elb_create_target_group_arn,
    ("elasticfilesystem.amazonaws.com", "CreateFileSystem"): extract_efs_create_file_system_id,
    ("sns.amazonaws.com", "CreateTopic"): extract_sns_create_topic_arn,
    ("sqs.amazonaws.com", "CreateQueue"): extract_sqs_create_queue_url,
    ("secretsmanager.amazonaws.com", "CreateSecret"): extract_secretsmanager_create_secret_arn,
    ("es.amazonaws.com", "CreateDomain"): extract_opensearch_create_domain_arn,
    ("ecs.amazonaws.com", "CreateCluster"): extract_ecs_create_cluster_arn,
    ("states.amazonaws.com", "CreateStateMachine"): extract_stepfunctions_create_state_machine_arn,
}
