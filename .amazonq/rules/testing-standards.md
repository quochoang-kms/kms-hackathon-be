# Testing Standards

## Test Structure
- Place tests in `tests/` directory
- Mirror source directory structure
- Use `.test.js` suffix for test files

## Testing Framework
- Use Jest for unit testing
- Mock AWS SDK services
- Test both success and error scenarios

## Test Coverage Requirements
- All Lambda handlers must have tests
- Test input validation
- Test database operations
- Test error handling
- Minimum 80% code coverage

## Mock Patterns
```javascript
// Mock AWS SDK
jest.mock('@aws-sdk/lib-dynamodb');

// Mock environment variables
process.env.TABLE_NAME = 'test-table';
```

## Test Naming
- Describe what is being tested
- Use "should" statements
- Group related tests with describe blocks

## Assertions
- Test response status codes
- Validate response body structure
- Check error messages
- Verify database calls made