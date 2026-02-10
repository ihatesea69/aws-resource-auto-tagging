us-east-1import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    print("Event received:")
    print(json.dumps(event))

    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    detail = event.get("detail", event)
    event_source = detail.get("eventSource")
    event_name = detail.get("eventName")
    if event_source == "s3.amazonaws.com" and event_name == "CreateBucket":
        try:
            # Extract bucket name from the event
            bucket_name = detail["requestParameters"]["bucketName"]
            
            # Create tags based on user identity
            user_identity = detail.get("userIdentity", {})
            tags = {
                "Owner": user_identity.get("userName", "Unknown"),
                "CreatedBy": user_identity.get("arn", "Unknown"),
                "AutoTagged": "true"
            }
            
            print(f"Applying tags to bucket: {bucket_name}")
            print(f"Tags: {tags}")
            
            # Apply tags to the S3 bucket
            s3.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={"TagSet": [{"Key": k, "Value": v} for k, v in tags.items()]}
            )
            
            print(f"Successfully tagged bucket: {bucket_name}")
            
        except Exception as e:
            print(f"Error tagging bucket: {str(e)}")
            raise e   
    try:
        # Extract instance ID from the event (EventBridge will pass this)
        # For testing, we'll use your specific instance
        instance_id = 'i-11111111111'
        
        # If this comes from EventBridge CloudTrail event
        if 'detail' in event:
            # Extract instance ID from CloudTrail event
            response_elements = event['detail'].get('responseElements', {})
            instances = response_elements.get('instancesSet', {}).get('items', [])
            if instances:
                instance_id = instances[0].get('instanceId')
        
        # Get current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get user identity from CloudTrail event
        user_name = "unknown"
        if 'detail' in event and 'userIdentity' in event['detail']:
            user_identity = event['detail']['userIdentity']
            if user_identity.get('type') == 'IAMUser':
                user_name = user_identity.get('userName', 'unknown')
            elif user_identity.get('type') == 'AssumedRole':
                # Extract username from assumed role ARN
                arn = user_identity.get('arn', '')
                if 'assumed-role' in arn:
                    user_name = arn.split('/')[-1]
        detail = event.get("detail", event)
        user_identity = detail.get("userIdentity", {})
        # Define tags to apply
        tags = [
            {
                'Key': 'Owner',
                'Value': user_name
            },
            {
                'Key': 'CreatedBy',
                'Value': user_identity.get("arn", "Unknown"),
            },
            {
                'Key': 'CreationDate',
                'Value': current_time
            },
            {
                'Key': 'Environment',
                'Value': 'Development'  # You can make this dynamic
            },
            {
                'Key': 'Project',
                'Value': 'CostTracking'
            },
            {
                'Key': 'AutoTagged',
                'Value': 'true'
            }
        ]
        
        # Apply tags to the instance
        response = ec2.create_tags(
            Resources=[instance_id],
            Tags=tags
        )
        
        print(f"Successfully tagged instance {acinstance_id} with tags: {tags}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully tagged instance {instance_id}',
                'instance_id': instance_id,
                'tags_applied': tags,
                'user': user_name
            })
        }
        
    except Exception as e:
        print(f"Error tagging instance: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to tag instance'
            })
        }
