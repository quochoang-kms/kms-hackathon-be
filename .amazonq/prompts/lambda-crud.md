# Lambda CRUD Function Generator

When creating CRUD Lambda functions, follow this template:

## Requirements
- Use async/await pattern
- Include comprehensive error handling
- Validate input parameters
- Use DynamoDBDocumentClient
- Return consistent response format
- Add CloudWatch logging
- Include request ID in error responses

## Template Structure
1. Import required AWS SDK modules
2. Initialize DynamoDB client outside handler
3. Validate environment variables
4. Implement input validation
5. Execute database operation
6. Return formatted response
7. Handle all error scenarios

## Naming Conventions
- Handler file: `[operation].js` (create.js, read.js, update.js, delete.js)
- Function name: `exports.handler`
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE

## Response Codes
- 200: Success with data
- 201: Created successfully
- 204: Success without data (delete)
- 400: Bad request/validation error
- 404: Resource not found
- 500: Internal server error