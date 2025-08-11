# Interview Generation Agent Instructions

## Overview
This document provides instructions for implementing an interview generation agent using the Strands Agents framework. The agent will utilize Amazon Bedrock LLM models and implement a multi-agent graph architecture to generate interview questions and sample answers based on job descriptions, CVs, role requirements, experience level, and interview round.

## Architecture Components

### 1. Multi-Agent Graph Structure
- **Document Processor Agent**: Extracts and analyzes content from JD and CV files (PDF, DOCX)
- **Question Generator Agent**: Creates relevant interview questions based on role, level, and round
- **Answer Generator Agent**: Generates sample answers for the created questions
- **Coordinator Agent**: Orchestrates the workflow and ensures quality output

### 2. Input Processing
- **Job Description (JD)**: Text or document file containing job requirements
- **CV/Resume**: PDF or DOCX file containing candidate information
- **Role**: Position type (e.g., Software Engineer, Data Scientist, Product Manager)
- **Level**: Experience level (Junior, Mid, Senior, Lead, Principal)
- **Round Number**: Interview stage (1st round - screening, 2nd round - technical, 3rd round - behavioral, etc.)

### 3. Output Generation
- **Questions Set**: Tailored interview questions based on inputs
- **Sample Answers**: Well-structured answers that demonstrate expected responses

## Implementation Requirements

### Dependencies
```
strands-agents>=0.1.0
strands-agents-tools>=0.1.0
boto3>=1.34.0
PyPDF2>=3.0.0
python-docx>=0.8.11
```

### AWS Configuration
- Amazon Bedrock model access enabled
- Appropriate IAM permissions for Bedrock API calls
- Region configuration (recommend us-west-2 for Claude models)

### File Structure
```
interview_agent/
├── __init__.py
├── agents/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── question_generator.py
│   ├── answer_generator.py
│   └── coordinator.py
├── tools/
│   ├── __init__.py
│   ├── document_parser.py
│   └── content_analyzer.py
├── utils/
│   ├── __init__.py
│   └── file_handlers.py
├── main.py
└── requirements.txt
```

### Key Features to Implement

1. **Document Processing**
   - PDF text extraction using PyPDF2
   - DOCX content parsing using python-docx
   - Content cleaning and structuring

2. **Multi-Agent Coordination**
   - Use Strands `agent_graph` tool for orchestration
   - Implement workflow management between agents
   - Handle data passing between agents

3. **Question Generation Logic**
   - Role-specific question templates
   - Level-appropriate difficulty scaling
   - Round-specific focus areas (technical, behavioral, cultural fit)

4. **Answer Generation**
   - STAR method for behavioral questions
   - Technical depth appropriate to level
   - Industry best practices incorporation

5. **Quality Assurance**
   - Question relevance validation
   - Answer quality assessment
   - Output formatting and structure

### Model Configuration
- Primary Model: Claude 3.7 Sonnet via Amazon Bedrock
- Fallback Model: Claude 3.5 Sonnet
- Temperature: 0.3 for consistency
- Max Tokens: 4000 for comprehensive responses

### Error Handling
- File format validation
- Content extraction error handling
- Model API error recovery
- Graceful degradation for missing inputs

### Testing Strategy
- Unit tests for individual agents
- Integration tests for multi-agent workflows
- Sample data validation
- Performance benchmarking

## Usage Example
```python
from interview_agent import InterviewAgent

agent = InterviewAgent()

result = agent.generate_interview_content(
    jd_file="path/to/job_description.pdf",
    cv_file="path/to/resume.pdf",
    role="Senior Software Engineer",
    level="Senior",
    round_number=2
)

print("Generated Questions:")
for q in result.questions:
    print(f"- {q}")

print("\nSample Answers:")
for a in result.answers:
    print(f"- {a}")
```

## Performance Considerations
- Implement caching for repeated document processing
- Optimize token usage for cost efficiency
- Consider async processing for large documents
- Implement rate limiting for API calls

## Security & Privacy
- Sanitize sensitive information from documents
- Implement secure file handling
- Ensure compliance with data protection regulations
- Use environment variables for API keys
