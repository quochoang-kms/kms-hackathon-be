# Project Implementation Guidelines

## Architecture
- Use AWS Lambda for serverless functions
- DynamoDB for data persistence
- API Gateway for REST endpoints
- Follow microservices pattern

## Code Structure
- Place Lambda functions in `src/lambdas/[feature]/`
- Use separate files for each HTTP method
- Include handler, business logic, and validation layers

## Error Handling
- Always wrap handlers in try-catch blocks
- Return consistent error response format
- Log errors with context information
- Use appropriate HTTP status codes

## Response Format
```javascript
// Success Response
{
  statusCode: 200,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data: result })
}

// Error Response
{
  statusCode: 500,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ error: error.message, requestId: context.awsRequestId })
}
```

## Environment Variables
- Use `process.env.TABLE_NAME` for DynamoDB tables
- Use `process.env.REGION` for AWS region
- Validate required environment variables at startup

## Security
- Validate all input parameters
- Sanitize data before database operations
- Use least privilege IAM policies
- Never log sensitive information