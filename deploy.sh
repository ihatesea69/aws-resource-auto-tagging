#!/bin/bash
# Deploy the AutoTag System to all three target regions.
# Usage: ./deploy.sh [EnvironmentName] [ProjectName]

set -e

ENVIRONMENT_NAME="${1:-Development}"
PROJECT_NAME="${2:-CostTracking}"
STACK_NAME="AutoTagSystem"
REGIONS=("us-east-1" "ap-southeast-1" "ap-southeast-2")

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Packaging Lambda code..."
(cd src && zip -r ../autotag-lambda.zip .)

for REGION in "${REGIONS[@]}"; do
  echo ""
  echo "=== Deploying to ${REGION} ==="

  CODE_BUCKET="autotag-code-${ACCOUNT_ID}-${REGION}"

  echo "Creating code bucket ${CODE_BUCKET} (if needed)..."
  aws s3 mb "s3://${CODE_BUCKET}" --region "${REGION}" 2>/dev/null || true

  echo "Uploading Lambda code..."
  aws s3 cp autotag-lambda.zip "s3://${CODE_BUCKET}/autotag-lambda.zip" --region "${REGION}"

  echo "Deploying CloudFormation stack..."
  aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name "${STACK_NAME}" \
    --capabilities CAPABILITY_NAMED_IAM \
    --region "${REGION}" \
    --parameter-overrides \
      EnvironmentName="${ENVIRONMENT_NAME}" \
      ProjectName="${PROJECT_NAME}"

  echo "=== ${REGION} deployment complete ==="
done

echo ""
echo "All regions deployed successfully."
echo "Environment: ${ENVIRONMENT_NAME}"
echo "Project: ${PROJECT_NAME}"
