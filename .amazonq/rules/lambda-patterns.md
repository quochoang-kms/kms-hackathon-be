# AWS Lambda Implementation Patterns

## Handler Structure
```javascript
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

exports.handler = async (event, context) => {
  try {
    // Input validation
    // Business logic
    // Database operations
    // Return response
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        error: error.message,
        requestId: context.awsRequestId 
      })
    };
  }
};
```

## DynamoDB Operations
- Use DynamoDBDocumentClient for simplified operations
- Always specify TableName from environment variables
- Include proper error handling for AWS SDK operations
- Use consistent key naming (id, createdAt, updatedAt)

## Input Validation
- Validate path parameters exist
- Check required body fields
- Sanitize input data
- Return 400 for validation errors

## Logging
- Log function entry with event details
- Log important business logic steps
- Log errors with full context
- Use structured logging format