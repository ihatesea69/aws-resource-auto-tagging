"""EC2 service handlers for auto-tagging."""

import logging
import boto3
try:
    from tag_serializer import serialize_ec2_tags
    from error_handler import handle_tagging_errors
except ImportError:
    from src.tag_serializer import serialize_ec2_tags
    from src.error_handler import handle_tagging_errors

logger = logging.getLogger(__name__)


def _get_ec2_client(detail):
    region = detail.get("awsRegion", None)
    return boto3.client("ec2", region_name=region) if region else boto3.client("ec2")


@handle_tagging_errors("RunInstances")
def handle_ec2_run_instances(detail, tags):
    response_elements = detail.get("responseElements", {})
    items = response_elements.get("instancesSet", {}).get("items", [])
    resource_ids = []
    for item in items:
        iid = item.get("instanceId")
        if iid:
            resource_ids.append(iid)
        for bd in item.get("blockDeviceMapping", {}).get("items", []):
            vid = bd.get("ebs", {}).get("volumeId")
            if vid:
                resource_ids.append(vid)
    if not resource_ids:
        logger.warning("No instance or volume IDs found in RunInstances event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=resource_ids, Tags=serialize_ec2_tags(tags))
    logger.info("Tagged EC2 resources: %s", resource_ids)


@handle_tagging_errors("CreateSecurityGroup")
def handle_ec2_create_security_group(detail, tags):
    group_id = detail.get("responseElements", {}).get("groupId")
    if not group_id:
        logger.warning("No groupId found in CreateSecurityGroup event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[group_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged security group: %s", group_id)


@handle_tagging_errors("CreateImage")
def handle_ec2_create_image(detail, tags):
    image_id = detail.get("responseElements", {}).get("imageId")
    if not image_id:
        logger.warning("No imageId found in CreateImage event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[image_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged AMI: %s", image_id)


@handle_tagging_errors("CreateVolume")
def handle_ec2_create_volume(detail, tags):
    volume_id = detail.get("responseElements", {}).get("volumeId")
    if not volume_id:
        logger.warning("No volumeId found in CreateVolume event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[volume_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged volume: %s", volume_id)


@handle_tagging_errors("CreateSnapshot")
def handle_ec2_create_snapshot(detail, tags):
    snapshot_id = detail.get("responseElements", {}).get("snapshotId")
    if not snapshot_id:
        logger.warning("No snapshotId found in CreateSnapshot event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[snapshot_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged snapshot: %s", snapshot_id)


@handle_tagging_errors("AllocateAddress")
def handle_ec2_allocate_address(detail, tags):
    allocation_id = detail.get("responseElements", {}).get("allocationId")
    if not allocation_id:
        logger.warning("No allocationId found in AllocateAddress event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[allocation_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged Elastic IP: %s", allocation_id)


@handle_tagging_errors("CreateNetworkInterface")
def handle_ec2_create_network_interface(detail, tags):
    eni_id = detail.get("responseElements", {}).get("networkInterface", {}).get("networkInterfaceId")
    if not eni_id:
        logger.warning("No networkInterfaceId found in CreateNetworkInterface event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[eni_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged ENI: %s", eni_id)


@handle_tagging_errors("CreateVpc")
def handle_ec2_create_vpc(detail, tags):
    vpc_id = detail.get("responseElements", {}).get("vpc", {}).get("vpcId")
    if not vpc_id:
        logger.warning("No vpcId found in CreateVpc event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[vpc_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged VPC: %s", vpc_id)


@handle_tagging_errors("CreateSubnet")
def handle_ec2_create_subnet(detail, tags):
    subnet_id = detail.get("responseElements", {}).get("subnet", {}).get("subnetId")
    if not subnet_id:
        logger.warning("No subnetId found in CreateSubnet event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[subnet_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged subnet: %s", subnet_id)


@handle_tagging_errors("CreateInternetGateway")
def handle_ec2_create_internet_gateway(detail, tags):
    igw_id = detail.get("responseElements", {}).get("internetGateway", {}).get("internetGatewayId")
    if not igw_id:
        logger.warning("No internetGatewayId found in CreateInternetGateway event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[igw_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged internet gateway: %s", igw_id)


@handle_tagging_errors("CreateNatGateway")
def handle_ec2_create_nat_gateway(detail, tags):
    nat_id = detail.get("responseElements", {}).get("natGateway", {}).get("natGatewayId")
    if not nat_id:
        logger.warning("No natGatewayId found in CreateNatGateway event")
        return
    ec2 = _get_ec2_client(detail)
    ec2.create_tags(Resources=[nat_id], Tags=serialize_ec2_tags(tags))
    logger.info("Tagged NAT gateway: %s", nat_id)
