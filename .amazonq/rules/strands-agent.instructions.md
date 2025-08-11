# Strands Agents Python Implementation Instructions

## Overview
Implement a multi-agent system using Strands Agents framework (Python) for interview question generation with AWS Bedrock integration.

## Architecture Pattern
- Use Strands Agents Graph for multi-agent orchestration in Python
- Integrate AWS Bedrock for LLM capabilities
- Process documents (PDF, DOCX) for CV parsing
- Generate structured interview questions and sample answers

## Agent Structure
```python
# Main Generation Agent with sub-agents:
# 1. DocumentParserAgent - Extract text from CV/JD files
# 2. QuestionGeneratorAgent - Generate interview questions
# 3. AnswerGeneratorAgent - Generate sample answers
```

## Input Processing
- JD (Job Description): Text or document
- CV: PDF/DOCX file processing
- Role: String (e.g., "Software Engineer", "Data Scientist")
- Level: String (e.g., "Junior", "Mid", "Senior")
- Round Number: Integer (1, 2, 3...)

## Output Format
```python
{
    "questions": [
        {
            "id": "string",
            "question": "string",
            "category": "string",
            "difficulty": "string",
            "expected_duration": int
        }
    ],
    "sample_answers": [
        {
            "question_id": "string",
            "answer": "string",
            "key_points": ["string"],
            "evaluation_criteria": ["string"]
        }
    ]
}
```

## Dependencies
- strandsagents
- boto3 (for Bedrock)
- PyPDF2 (for PDF processing)
- python-docx (for DOCX processing)

## Implementation Guidelines
- Use async/await for all agent operations
- Implement proper error handling for document parsing
- Use structured prompts for consistent LLM outputs
- Implement retry logic for Bedrock API calls
- Follow AWS Lambda patterns for serverless deployment

## Security Considerations
- Validate file types and sizes
- Sanitize extracted text content
- Use IAM roles for Bedrock access
- Implement rate limiting for API calls