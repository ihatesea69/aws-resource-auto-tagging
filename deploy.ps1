# Deploy the AutoTag System to all three target regions.
# Usage: .\deploy.ps1 [-EnvironmentName "Development"] [-ProjectName "CostTracking"]

param(
    [string]$EnvironmentName = "Development",
    [string]$ProjectName = "CostTracking"
)

$ErrorActionPreference = "Stop"

$StackName = "AutoTagSystem"
$Regions = @("us-east-1", "ap-southeast-1", "ap-southeast-2")

$AccountId = aws sts get-caller-identity --query Account --output text
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to get AWS account ID. Check your AWS CLI credentials."
    exit 1
}

Write-Host "Packaging Lambda code..."
if (Test-Path "autotag-lambda.zip") { Remove-Item "autotag-lambda.zip" }
Compress-Archive -Path "src\*" -DestinationPath "autotag-lambda.zip" -Force

foreach ($Region in $Regions) {
    Write-Host ""
    Write-Host "=== Deploying to $Region ==="

    $CodeBucket = "autotag-code-$AccountId-$Region"

    Write-Host "Creating code bucket $CodeBucket (if needed)..."
    aws s3 mb "s3://$CodeBucket" --region $Region 2>$null
    # Ignore error if bucket already exists

    Write-Host "Uploading Lambda code..."
    aws s3 cp autotag-lambda.zip "s3://$CodeBucket/autotag-lambda.zip" --region $Region
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to upload Lambda code to $Region"
        exit 1
    }

    Write-Host "Deploying CloudFormation stack..."
    aws cloudformation deploy `
        --template-file template.yaml `
        --stack-name $StackName `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region `
        --parameter-overrides `
        "EnvironmentName=$EnvironmentName" `
        "ProjectName=$ProjectName"

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to deploy stack in $Region"
        exit 1
    }

    Write-Host "=== $Region deployment complete ==="
}

Write-Host ""
Write-Host "All regions deployed successfully."
Write-Host "Environment: $EnvironmentName"
Write-Host "Project: $ProjectName"
