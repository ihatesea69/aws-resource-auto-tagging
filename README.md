<p align="center">
  <img src="docs/assets/logo.svg" alt="AutoTag" width="120" />
</p>

<h1 align="center">AutoTag</h1>

<p align="center">
  <strong>Automatically tag every new AWS resource with owner, environment, and project metadata.</strong>
</p>

<p align="center">
  <a href="https://github.com/ihatesea69/aws-autotag/actions"><img src="https://img.shields.io/github/actions/workflow/status/ihatesea69/aws-autotag/ci.yml?branch=main&style=flat-square&logo=github" alt="CI"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://aws.amazon.com/cloudformation/"><img src="https://img.shields.io/badge/IaC-CloudFormation-FF9900.svg?style=flat-square&logo=amazonaws&logoColor=white" alt="CloudFormation"></a>
  <a href="https://github.com/ihatesea69/aws-autotag/stargazers"><img src="https://img.shields.io/github/stars/ihatesea69/aws-autotag?style=flat-square&logo=github" alt="Stars"></a>
  <a href="https://github.com/ihatesea69/aws-autotag/issues"><img src="https://img.shields.io/github/issues/ihatesea69/aws-autotag?style=flat-square" alt="Issues"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-supported-services">Supported Services</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## The Problem

AWS resources created without tags become invisible to cost allocation, security audits, and operational dashboards. Manual tagging is error-prone and rarely enforced. Teams end up with thousands of untagged resources and no idea who created them or why.

## The Solution

**AutoTag** is a zero-touch, event-driven tagging system. It listens for resource creation events via CloudTrail + EventBridge and automatically applies a standard tag set — including the creator's identity — within seconds of resource creation. Deploy once per region, forget about it.


### Tags Applied

| Tag | Value | Example |
|-----|-------|---------|
| `Owner` | IAM user / role session name | `alice` |
| `CreatedBy` | Full ARN of the creator | `arn:aws:iam::123456789012:user/alice` |
| `CreationDate` | ISO 8601 timestamp | `2026-02-10T08:30:00Z` |
| `Environment` | Configurable per stack | `Production` |
| `Project` | Configurable per stack | `CostTracking` |
| `AutoTagged` | Always `true` | `true` |

---

## 🏗 Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  User creates │────▶│   CloudTrail     │────▶│   EventBridge     │
│  AWS resource │     │   (write events) │     │   (25 event rules)│
└──────────────┘     └──────────────────┘     └─────────┬─────────┘
                                                        │
                                                        ▼
                                              ┌───────────────────┐
                                              │  AutoTag Lambda   │
                                              │                   │
                                              │  1. Extract ID    │
                                              │  2. Resolve owner │
                                              │  3. Build tags    │
                                              │  4. Apply tags    │
                                              └───────────────────┘
```

**Single CloudFormation stack per region** — deploys CloudTrail trail, EventBridge rule, Lambda function, IAM role, and CloudWatch log group.

---

## 🎯 Supported Services

<table>
<tr><th>Service</th><th>Events</th><th>Resources Tagged</th></tr>
<tr><td rowspan="11"><strong>EC2</strong></td><td>RunInstances</td><td>Instances + Volumes</td></tr>
<tr><td>CreateSecurityGroup</td><td>Security Group</td></tr>
<tr><td>CreateImage</td><td>AMI</td></tr>
<tr><td>CreateVolume</td><td>EBS Volume</td></tr>
<tr><td>CreateSnapshot</td><td>EBS Snapshot</td></tr>
<tr><td>AllocateAddress</td><td>Elastic IP</td></tr>
<tr><td>CreateNetworkInterface</td><td>ENI</td></tr>
<tr><td>CreateVpc</td><td>VPC</td></tr>
<tr><td>CreateSubnet</td><td>Subnet</td></tr>
<tr><td>CreateInternetGateway</td><td>Internet Gateway</td></tr>
<tr><td>CreateNatGateway</td><td>NAT Gateway</td></tr>
<tr><td><strong>S3</strong></td><td>CreateBucket</td><td>S3 Bucket</td></tr>
<tr><td rowspan="2"><strong>RDS</strong></td><td>CreateDBInstance</td><td>DB Instance</td></tr>
<tr><td>CreateDBCluster</td><td>DB Cluster</td></tr>
<tr><td><strong>DynamoDB</strong></td><td>CreateTable</td><td>Table</td></tr>
<tr><td><strong>Lambda</strong></td><td>CreateFunction</td><td>Function</td></tr>
<tr><td rowspan="2"><strong>ELB</strong></td><td>CreateLoadBalancer</td><td>Load Balancer</td></tr>
<tr><td>CreateTargetGroup</td><td>Target Group</td></tr>
<tr><td><strong>EFS</strong></td><td>CreateFileSystem</td><td>File System</td></tr>
<tr><td><strong>SNS</strong></td><td>CreateTopic</td><td>Topic</td></tr>
<tr><td><strong>SQS</strong></td><td>CreateQueue</td><td>Queue</td></tr>
<tr><td><strong>Secrets Manager</strong></td><td>CreateSecret</td><td>Secret</td></tr>
<tr><td><strong>OpenSearch</strong></td><td>CreateDomain</td><td>Domain</td></tr>
<tr><td><strong>ECS</strong></td><td>CreateCluster</td><td>Cluster</td></tr>
<tr><td><strong>Step Functions</strong></td><td>CreateStateMachine</td><td>State Machine</td></tr>
</table>

> **25 events** across **13 AWS services** — covers the most commonly created resources.

---

## 🚀 Quick Start

### Prerequisites

- AWS CLI v2 configured with credentials
- Python 3.12+
- An AWS account with CloudTrail and EventBridge enabled

### One-Command Deploy

```bash
# Linux / macOS
chmod +x deploy.sh
./deploy.sh

# Windows PowerShell
.\deploy.ps1
```

This packages the Lambda, creates S3 code buckets, and deploys CloudFormation stacks to `us-east-1`, `ap-southeast-1`, and `ap-southeast-2`.

---

## 📦 Deployment

### Step-by-Step

**1. Package the Lambda**

```bash
cd src && zip -r ../autotag-lambda.zip . && cd ..
```

**2. Upload to S3 (each region)**

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

for REGION in us-east-1 ap-southeast-1 ap-southeast-2; do
  aws s3 mb s3://autotag-code-${ACCOUNT_ID}-${REGION} --region ${REGION} 2>/dev/null
  aws s3 cp autotag-lambda.zip s3://autotag-code-${ACCOUNT_ID}-${REGION}/autotag-lambda.zip --region ${REGION}
done
```

**3. Deploy CloudFormation**

```bash
for REGION in us-east-1 ap-southeast-1 ap-southeast-2; do
  aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name AutoTagSystem \
    --capabilities CAPABILITY_NAMED_IAM \
    --region ${REGION} \
    --parameter-overrides \
      EnvironmentName=Production \
      ProjectName=MyProject
done
```

---

## ⚙ Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EnvironmentName` | `Development` | Value for the `Environment` tag |
| `ProjectName` | `CostTracking` | Value for the `Project` tag |

Pass these as `--parameter-overrides` during CloudFormation deploy.

---

## 🧩 Project Structure

```
aws-autotag/
├── src/
│   ├── lambda_function.py    # Lambda entry point
│   ├── config.py             # Event → handler mapping
│   ├── identity.py           # CloudTrail identity extraction
│   ├── tag_builder.py        # Standard tag set construction
│   ├── tag_serializer.py     # Tag format conversion per service
│   ├── tag_printer.py        # Human-readable tag formatting
│   ├── resource_extractors.py# Pure resource ID extraction
│   ├── error_handler.py      # Decorator for error handling
│   ├── retry.py              # Exponential backoff for throttling
│   └── handlers/
│       ├── ec2.py            # EC2 tagging (11 events)
│       ├── s3.py             # S3 tagging (merge existing tags)
│       ├── rds.py            # RDS tagging
│       └── other_services.py # DynamoDB, Lambda, ELB, EFS, SNS, SQS, etc.
├── tests/
│   ├── test_identity.py
│   ├── test_tag_builder.py
│   ├── test_tag_serializer.py
│   ├── test_tag_printer.py
│   ├── test_resource_extraction.py
│   └── test_error_handling.py
├── template.yaml             # CloudFormation template
├── deploy.sh                 # Bash deploy script
├── deploy.ps1                # PowerShell deploy script
└── requirements.txt
```

---

## 🔧 Extending AutoTag

Adding a new service takes ~15 minutes:

1. Add a handler function in `src/handlers/`
2. Add a resource extractor in `src/resource_extractors.py`
3. Register the `(eventSource, eventName)` in `src/config.py`
4. Add the event to the EventBridge rule in `template.yaml`
5. Add IAM permissions to the Lambda role in `template.yaml`
6. Write tests and update this README

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## 🧪 Testing

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

Tests include unit tests and property-based tests (via Hypothesis) for identity extraction, tag building, serialization round-trips, and resource extraction.

---

## 🔍 Troubleshooting

| Symptom | Check |
|---------|-------|
| Tags not appearing | CloudWatch Logs at `/aws/lambda/AutoTagLambda-{Region}` |
| EventBridge not firing | Verify rule is ENABLED in EventBridge console |
| Permission denied | Lambda IAM role missing tagging permission for the service |
| Throttling errors | Lambda retries 3× with exponential backoff (1s → 2s → 4s) |
| Stack deploy fails | Ensure S3 code bucket exists and contains `autotag-lambda.zip` |

---

## 🧹 Cleanup

```bash
for REGION in us-east-1 ap-southeast-1 ap-southeast-2; do
  aws cloudformation delete-stack --stack-name AutoTagSystem --region ${REGION}
  aws cloudformation wait stack-delete-complete --stack-name AutoTagSystem --region ${REGION}
done
```

> Empty the CloudTrail S3 bucket before deleting the stack, or the delete will fail.

---

## 🗺 Roadmap

- [ ] Support for additional services (Kinesis, Redshift, CloudFront)
- [ ] Slack/Teams notification on tagging events
- [ ] Tag compliance dashboard
- [ ] Custom tag rules via DynamoDB configuration
- [ ] Multi-account support via AWS Organizations

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting a PR.

---

<p align="center">
  <a href="https://star-history.com/#ihatesea69/aws-autotag&Date">
    <img src="https://api.star-history.com/svg?repos=ihatesea69/aws-autotag&type=Date&theme=dark" alt="Star History Chart" width="600" />
  </a>
</p>

<p align="center">
  If AutoTag saves you time, consider giving it a ⭐
</p>
