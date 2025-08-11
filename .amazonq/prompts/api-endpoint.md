# API Endpoint Generator

Generate complete API endpoint with:

## Components Required
- Lambda handler function
- Input validation schema
- Database operations
- Error handling
- Response formatting
- Unit tests

## Implementation Pattern
```javascript
// 1. Imports and client setup
// 2. Input validation function
// 3. Main handler with try-catch
// 4. Database operation
// 5. Response formatting
```

## Validation Rules
- Check required fields exist
- Validate data types
- Sanitize input values
- Return 400 for invalid input

## Database Operations
- Use environment variables for table names
- Include proper error handling
- Log operations for debugging
- Handle AWS SDK exceptions

## Testing Requirements
- Unit tests for handler
- Mock AWS SDK calls
- Test error scenarios
- Validate response format