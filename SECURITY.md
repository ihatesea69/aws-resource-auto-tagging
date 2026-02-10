# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainers at: **[security contact email]**
3. Include a description of the vulnerability and steps to reproduce
4. Allow reasonable time for a fix before public disclosure

## Security Considerations

- The Lambda function requires broad tagging permissions across services. Follow the principle of least privilege and restrict `Resource` ARNs where possible.
- CloudTrail logs may contain sensitive metadata. Ensure the trail S3 bucket has appropriate access controls.
- Review IAM role permissions regularly and remove unused service permissions.
- Use AWS CloudFormation stack policies to prevent unauthorized modifications.

## Best Practices

- Deploy in a dedicated AWS account or use SCPs to limit blast radius
- Enable S3 bucket versioning and encryption on the CloudTrail log bucket
- Monitor CloudWatch Logs for unexpected errors or access patterns
- Rotate credentials and review IAM policies periodically
