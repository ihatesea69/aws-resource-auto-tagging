"""Service handler configuration mapping CloudTrail events to handler functions."""

from src.handlers.ec2 import (
    handle_ec2_run_instances,
    handle_ec2_create_security_group,
    handle_ec2_create_image,
    handle_ec2_create_volume,
    handle_ec2_create_snapshot,
    handle_ec2_allocate_address,
    handle_ec2_create_network_interface,
    handle_ec2_create_vpc,
    handle_ec2_create_subnet,
    handle_ec2_create_internet_gateway,
    handle_ec2_create_nat_gateway,
)
from src.handlers.s3 import handle_s3_create_bucket
from src.handlers.rds import (
    handle_rds_create_db_instance,
    handle_rds_create_db_cluster,
)
from src.handlers.other_services import (
    handle_dynamodb_create_table,
    handle_lambda_create_function,
    handle_elb_create_load_balancer,
    handle_elb_create_target_group,
    handle_efs_create_file_system,
    handle_sns_create_topic,
    handle_sqs_create_queue,
    handle_secretsmanager_create_secret,
    handle_opensearch_create_domain,
    handle_ecs_create_cluster,
    handle_stepfunctions_create_state_machine,
)

# Maps (eventSource, eventName) -> handler callable for all 25 supported events
SERVICE_HANDLERS = {
    # EC2 events (11)
    ("ec2.amazonaws.com", "RunInstances"): handle_ec2_run_instances,
    ("ec2.amazonaws.com", "CreateSecurityGroup"): handle_ec2_create_security_group,
    ("ec2.amazonaws.com", "CreateImage"): handle_ec2_create_image,
    ("ec2.amazonaws.com", "CreateVolume"): handle_ec2_create_volume,
    ("ec2.amazonaws.com", "CreateSnapshot"): handle_ec2_create_snapshot,
    ("ec2.amazonaws.com", "AllocateAddress"): handle_ec2_allocate_address,
    ("ec2.amazonaws.com", "CreateNetworkInterface"): handle_ec2_create_network_interface,
    ("ec2.amazonaws.com", "CreateVpc"): handle_ec2_create_vpc,
    ("ec2.amazonaws.com", "CreateSubnet"): handle_ec2_create_subnet,
    ("ec2.amazonaws.com", "CreateInternetGateway"): handle_ec2_create_internet_gateway,
    ("ec2.amazonaws.com", "CreateNatGateway"): handle_ec2_create_nat_gateway,
    # S3 events (1)
    ("s3.amazonaws.com", "CreateBucket"): handle_s3_create_bucket,
    # RDS events (2)
    ("rds.amazonaws.com", "CreateDBInstance"): handle_rds_create_db_instance,
    ("rds.amazonaws.com", "CreateDBCluster"): handle_rds_create_db_cluster,
    # DynamoDB events (1)
    ("dynamodb.amazonaws.com", "CreateTable"): handle_dynamodb_create_table,
    # Lambda events (1)
    ("lambda.amazonaws.com", "CreateFunction20150331"): handle_lambda_create_function,
    # ELB events (2)
    ("elasticloadbalancing.amazonaws.com", "CreateLoadBalancer"): handle_elb_create_load_balancer,
    ("elasticloadbalancing.amazonaws.com", "CreateTargetGroup"): handle_elb_create_target_group,
    # EFS events (1)
    ("elasticfilesystem.amazonaws.com", "CreateFileSystem"): handle_efs_create_file_system,
    # SNS events (1)
    ("sns.amazonaws.com", "CreateTopic"): handle_sns_create_topic,
    # SQS events (1)
    ("sqs.amazonaws.com", "CreateQueue"): handle_sqs_create_queue,
    # Secrets Manager events (1)
    ("secretsmanager.amazonaws.com", "CreateSecret"): handle_secretsmanager_create_secret,
    # OpenSearch events (1)
    ("es.amazonaws.com", "CreateDomain"): handle_opensearch_create_domain,
    # ECS events (1)
    ("ecs.amazonaws.com", "CreateCluster"): handle_ecs_create_cluster,
    # Step Functions events (1)
    ("states.amazonaws.com", "CreateStateMachine"): handle_stepfunctions_create_state_machine,
}
