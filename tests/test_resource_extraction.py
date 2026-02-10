"""Property test for resource ID extraction completeness."""

from hypothesis import given, settings, strategies as st, assume
from src.resource_extractors import EXTRACTORS

# A non-empty resource ID string
resource_id = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_:/"),
    min_size=1, max_size=64,
)


def build_detail_for_event(event_source, event_name, rid):
    """Build a well-formed CloudTrail detail dict for a given event with a valid resource ID."""
    key = (event_source, event_name)

    if key == ("ec2.amazonaws.com", "RunInstances"):
        return {"responseElements": {"instancesSet": {"items": [{"instanceId": rid}]}}}
    if key == ("ec2.amazonaws.com", "CreateSecurityGroup"):
        return {"responseElements": {"groupId": rid}}
    if key == ("ec2.amazonaws.com", "CreateImage"):
        return {"responseElements": {"imageId": rid}}
    if key == ("ec2.amazonaws.com", "CreateVolume"):
        return {"responseElements": {"volumeId": rid}}
    if key == ("ec2.amazonaws.com", "CreateSnapshot"):
        return {"responseElements": {"snapshotId": rid}}
    if key == ("ec2.amazonaws.com", "AllocateAddress"):
        return {"responseElements": {"allocationId": rid}}
    if key == ("ec2.amazonaws.com", "CreateNetworkInterface"):
        return {"responseElements": {"networkInterface": {"networkInterfaceId": rid}}}
    if key == ("ec2.amazonaws.com", "CreateVpc"):
        return {"responseElements": {"vpc": {"vpcId": rid}}}
    if key == ("ec2.amazonaws.com", "CreateSubnet"):
        return {"responseElements": {"subnet": {"subnetId": rid}}}
    if key == ("ec2.amazonaws.com", "CreateInternetGateway"):
        return {"responseElements": {"internetGateway": {"internetGatewayId": rid}}}
    if key == ("ec2.amazonaws.com", "CreateNatGateway"):
        return {"responseElements": {"natGateway": {"natGatewayId": rid}}}
    if key == ("s3.amazonaws.com", "CreateBucket"):
        return {"requestParameters": {"bucketName": rid}}
    if key == ("rds.amazonaws.com", "CreateDBInstance"):
        return {"responseElements": {"dBInstanceArn": rid}}
    if key == ("rds.amazonaws.com", "CreateDBCluster"):
        return {"responseElements": {"dBClusterArn": rid}}
    if key == ("dynamodb.amazonaws.com", "CreateTable"):
        return {"responseElements": {"tableDescription": {"tableArn": rid}}}
    if key == ("lambda.amazonaws.com", "CreateFunction20150331"):
        return {"responseElements": {"functionArn": rid}}
    if key == ("elasticloadbalancing.amazonaws.com", "CreateLoadBalancer"):
        return {"responseElements": {"loadBalancers": [{"loadBalancerArn": rid}]}}
    if key == ("elasticloadbalancing.amazonaws.com", "CreateTargetGroup"):
        return {"responseElements": {"targetGroups": [{"targetGroupArn": rid}]}}
    if key == ("elasticfilesystem.amazonaws.com", "CreateFileSystem"):
        return {"responseElements": {"fileSystemId": rid}}
    if key == ("sns.amazonaws.com", "CreateTopic"):
        return {"responseElements": {"topicArn": rid}}
    if key == ("sqs.amazonaws.com", "CreateQueue"):
        return {"responseElements": {"queueUrl": rid}}
    if key == ("secretsmanager.amazonaws.com", "CreateSecret"):
        return {"responseElements": {"aRN": rid}}
    if key == ("es.amazonaws.com", "CreateDomain"):
        return {"responseElements": {"domainStatus": {"aRN": rid}}}
    if key == ("ecs.amazonaws.com", "CreateCluster"):
        return {"responseElements": {"cluster": {"clusterArn": rid}}}
    if key == ("states.amazonaws.com", "CreateStateMachine"):
        return {"responseElements": {"stateMachineArn": rid}}
    raise ValueError(f"Unknown event: {key}")


EVENT_KEYS = list(EXTRACTORS.keys())


# Feature: auto-tag-resources, Property 5: Resource ID extraction completeness
@settings(max_examples=100)
@given(
    event_index=st.integers(min_value=0, max_value=len(EVENT_KEYS) - 1),
    rid=resource_id,
)
def test_resource_id_extraction_completeness(event_index, rid):
    """Property 5: Resource ID extraction completeness.

    For any supported CloudTrail event with well-formed responseElements,
    the extractor returns at least one non-empty resource identifier.
    **Validates: Requirements 4.1-4.11, 5.1, 6.1-6.2, 7.1, 8.1, 9.1-9.2, 10.1-10.7**
    """
    event_source, event_name = EVENT_KEYS[event_index]
    detail = build_detail_for_event(event_source, event_name, rid)
    extractor = EXTRACTORS[(event_source, event_name)]
    result = extractor(detail)

    # Result should be non-empty (either a non-empty string or a non-empty list)
    if isinstance(result, list):
        assert len(result) > 0, f"Extractor for {event_source}/{event_name} returned empty list"
        for item in result:
            assert item, f"Extractor for {event_source}/{event_name} returned empty item in list"
    else:
        assert result, f"Extractor for {event_source}/{event_name} returned empty/None"
