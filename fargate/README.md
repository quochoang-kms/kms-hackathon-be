# Interview Agent API - AWS Fargate Deployment

This project implements a scalable web API for the Interview Preparation System using AWS Fargate, following the [Strands Agents deployment guide](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_aws_fargate/).

## Architecture

The deployment consists of:

- **FastAPI Application**: RESTful API with multiple endpoints for interview preparation
- **AWS Fargate**: Serverless container platform for running the application
- **Application Load Balancer**: HTTP load balancer with health checks
- **Amazon ECS**: Container orchestration service
- **VPC**: Private networking with NAT gateway for outbound internet access
- **CloudWatch**: Logging and monitoring

## Features

### API Endpoints

1. **Health Check** (`GET /health`)
   - Service health monitoring
   - Used by load balancer health checks

2. **Interview Preparation** (`POST /prepare-interview`)
   - Full multi-agent workflow
   - Analyzes JD and CV
   - Generates tailored interview questions
   - Returns structured response

3. **File Upload** (`POST /prepare-interview-files`)
   - Accepts file uploads for JD and CV
   - Supports multiple file formats

4. **Streaming Response** (`POST /prepare-interview-stream`)
   - Real-time streaming of preparation process
   - Progress updates during execution

5. **Quick Analysis** (`POST /analyze`)
   - Lightweight analysis endpoint
   - Fast response for basic matching

### Multi-Agent System

The API orchestrates multiple specialized AI agents:

- **JD_ANALYZER**: Analyzes job descriptions
- **CV_ANALYZER**: Processes candidate CVs
- **SKILL_MATCHER**: Matches skills between JD and CV
- **QUESTION_GENERATOR**: Creates tailored interview questions

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker or Podman installed
- Node.js and AWS CDK v2 installed
- Python 3.12+ for local development

### Required AWS Permissions

Your AWS user/role needs permissions for:
- Amazon ECS (Fargate)
- Amazon EC2 (VPC, Security Groups, Load Balancer)
- Amazon ECR (Container Registry)
- Amazon Bedrock (AI model access)
- CloudWatch Logs
- IAM (for creating service roles)

## Quick Start

### 1. Deploy to AWS Fargate

```bash
# Clone and navigate to project
cd /path/to/kms-hackathon-be

# Run the deployment script
./deploy-fargate.sh
```

This script will:
- Bootstrap CDK if needed
- Build the Docker image
- Deploy the infrastructure
- Set up load balancer with health checks
- Output the service URL

### 2. Local Development

```bash
# Run locally for testing
./run-local.sh
```

This will:
- Create a virtual environment
- Install dependencies
- Start FastAPI server on http://localhost:8000

## Manual Deployment Steps

If you prefer manual deployment:

### 1. Install Dependencies

```bash
cd infrastructure
pip install -r requirements.txt
```

### 2. Bootstrap CDK

```bash
cdk bootstrap
```

### 3. Deploy Infrastructure

```bash
# Deploy the Fargate stack
cdk deploy InterviewAgentFargateStack --require-approval never
```

### 4. Get Service URL

```bash
# Get the load balancer DNS name
aws cloudformation describe-stacks \
  --stack-name InterviewAgentFargateStack \
  --query "Stacks[0].Outputs[?ExportName=='InterviewAgentServiceEndpoint'].OutputValue" \
  --output text
```

## Configuration

### Environment Variables

The application uses these environment variables:

- `MODEL_ID`: Bedrock model ID (default: claude-3-sonnet)
- `MODEL_ID2`: Secondary model ID
- `REGION_NAME`: AWS region (default: us-east-1)
- `LOG_LEVEL`: Logging level (default: INFO)

### Infrastructure Configuration

Key infrastructure settings in `interview_agent_fargate_stack.py`:

- **CPU**: 1024 (1 vCPU)
- **Memory**: 2048 MB
- **Desired Count**: 2 instances
- **Health Check**: `/health` endpoint
- **Platform**: ARM64 for cost optimization

## API Usage Examples

### 1. Health Check

```bash
curl http://your-load-balancer-url/health
```

### 2. Interview Preparation

```bash
curl -X POST http://your-load-balancer-url/prepare-interview \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We are looking for a Senior Python Developer with AWS experience...",
    "cv_content": "John Doe - 5 years Python development, AWS certified...",
    "additional_context": "Focus on system design and leadership skills"
  }'
```

### 3. File Upload

```bash
curl -X POST http://your-load-balancer-url/prepare-interview-files \
  -F "job_description=@job_description.txt" \
  -F "cv_file=@candidate_cv.pdf" \
  -F "additional_context=Technical interview focus"
```

### 4. Streaming Response

```bash
curl -X POST http://your-load-balancer-url/prepare-interview-stream \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Your JD here...",
    "cv_content": "Your CV here..."
  }'
```

## Monitoring and Troubleshooting

### CloudWatch Logs

View application logs:
```bash
aws logs tail /ecs/interview-agent --follow
```

### ECS Service Status

Check service status:
```bash
aws ecs describe-services \
  --cluster interview-agent-cluster \
  --services interview-agent-service
```

### Load Balancer Health

Check target health:
```bash
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/name/id
```

## Scaling

### Auto Scaling

The service can be configured for auto scaling based on:
- CPU utilization
- Memory utilization
- Request count
- Custom CloudWatch metrics

### Manual Scaling

Update desired count:
```bash
aws ecs update-service \
  --cluster interview-agent-cluster \
  --service interview-agent-service \
  --desired-count 4
```

## Security

- Service runs in private subnets
- Load balancer in public subnets only
- Security groups restrict traffic to necessary ports
- IAM roles follow least privilege principle
- No hardcoded credentials in code

## Cost Optimization

- ARM64 platform for lower costs
- Efficient container sizing
- CloudWatch log retention set to 1 week
- Consider Spot instances for non-production

## Cleanup

To remove all resources:

```bash
cdk destroy InterviewAgentFargateStack
```

## Troubleshooting

### Common Issues

1. **Deployment Fails**
   - Check AWS permissions
   - Verify Docker is running
   - Ensure CDK is bootstrapped

2. **Health Check Fails**
   - Check application logs in CloudWatch
   - Verify port configuration
   - Check security group rules

3. **High Memory Usage**
   - Consider increasing memory limit
   - Optimize agent initialization
   - Review model loading

### Support

For deployment issues:
1. Check CloudWatch logs
2. Review ECS service events
3. Verify AWS permissions
4. Test locally first

## Integration with Frontend

The API is designed to work with web frontends:

- CORS enabled for all origins
- JSON responses for easy parsing
- RESTful endpoints
- OpenAPI documentation at `/docs`

Example frontend integration:

```javascript
// Prepare interview
const response = await fetch('http://your-api-url/prepare-interview', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    job_description: jobDescription,
    cv_content: cvContent
  })
});

const result = await response.json();
console.log('Interview questions:', result.questions);
```

## Next Steps

Potential enhancements:
- Add authentication (API Gateway, Cognito)
- Implement rate limiting
- Add custom domain and HTTPS
- Set up CI/CD pipeline
- Add monitoring dashboards
- Implement caching layer
