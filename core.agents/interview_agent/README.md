# Interview Agent - Multi-Agent Interview Question & Answer Generator

A sophisticated multi-agent system built with Strands Agents framework that generates tailored interview questions and sample answers based on job descriptions, CVs, role requirements, experience levels, and interview rounds.

## 🌟 Features

- **Multi-Agent Architecture**: Coordinated workflow using specialized agents
- **Document Processing**: Supports PDF, DOCX, and text files
- **Intelligent Question Generation**: Role-specific, level-appropriate questions
- **Sample Answer Generation**: High-quality answers with evaluation criteria
- **Experience Level Adaptation**: Junior to Principal level support
- **Interview Round Focus**: Screening, Technical, Behavioral, and Final rounds
- **AWS Bedrock Integration**: Powered by Claude 3.7 Sonnet

## 🏗️ Architecture

The system uses a multi-agent architecture with four specialized agents:

1. **Document Processor Agent**: Extracts and analyzes JD and CV content
2. **Question Generator Agent**: Creates relevant interview questions
3. **Answer Generator Agent**: Generates comprehensive sample answers
4. **Coordinator Agent**: Orchestrates the entire workflow

## 📦 Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2
```

3. Enable Bedrock model access:
   - Go to AWS Bedrock console
   - Request access to Claude 3.7 Sonnet model
   - Follow [AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html)

## 🚀 Quick Start

### Basic Usage

```python
from interview_agent import InterviewAgent

# Initialize the agent
agent = InterviewAgent()

# Generate interview content
result = agent.generate_interview_content(
    jd_content="Your job description text here...",
    cv_content="Candidate's CV text here...",
    role="Senior Software Engineer",
    level="Senior",
    round_number=2,  # Technical round
    num_questions=5
)

# Access results
print("Questions:")
for question in result.questions:
    print(f"- {question.question}")

print("Sample Answers:")
for answer in result.sample_answers:
    print(f"Q: {answer.question}")
    print(f"A: {answer.answer}")
```

### Using Files

```python
from interview_agent import generate_interview

result = generate_interview(
    jd_file="job_description.pdf",
    cv_file="candidate_resume.pdf",
    role="Data Scientist",
    level="Mid",
    round_number=1,
    num_questions=4
)
```

## 📋 Supported Parameters

### Experience Levels
- `Junior`: Entry-level positions (0-2 years)
- `Mid`: Mid-level positions (2-5 years)
- `Senior`: Senior positions (5-8 years)
- `Lead`: Team lead positions (8+ years)
- `Principal`: Principal/Staff positions (10+ years)

### Interview Rounds
- `1` (Screening): Initial assessment, basic qualifications
- `2` (Technical): Deep technical evaluation
- `3` (Behavioral): Past experiences, soft skills
- `4` (Final): Strategic thinking, final assessment

### Supported File Types
- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Plain text (`.txt`, `.md`)

## 🔧 Advanced Usage

### Custom Model Configuration

```python
from interview_agent import InterviewAgent

agent = InterviewAgent(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region="us-east-1"
)
```

### Input Validation

```python
agent = InterviewAgent()

validation = agent.validate_inputs(
    role="Software Engineer",
    level="Senior",
    round_number=2
)

if validation['valid']:
    # Proceed with generation
    pass
else:
    print("Errors:", validation['errors'])
```

### Error Handling

```python
try:
    result = agent.generate_interview_content(
        jd_content=jd_text,
        cv_content=cv_text,
        role="Product Manager",
        level="Mid",
        round_number=3
    )
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Generation error: {e}")
```

## 📊 Output Structure

The system returns an `InterviewResponse` object with:

```python
class InterviewResponse:
    questions: List[InterviewQuestion]      # Generated questions
    sample_answers: List[SampleAnswer]      # Sample answers
    interview_focus: str                    # Round focus description
    preparation_tips: List[str]             # Interviewer tips
```

### Question Structure
```python
class InterviewQuestion:
    question: str                           # Question text
    type: str                              # technical/behavioral/situational/cultural_fit
    difficulty: str                        # basic/intermediate/advanced
    expected_duration: int                 # Minutes for answer
```

### Answer Structure
```python
class SampleAnswer:
    question: str                          # Original question
    answer: str                           # Sample answer
    key_points: List[str]                 # Key points to cover
    evaluation_criteria: List[str]        # What to evaluate
```

## 🎯 Examples

### Example 1: Technical Interview for Senior Engineer

```python
jd_content = """
Senior Backend Engineer
- 5+ years Python/Java experience
- Microservices architecture
- AWS cloud platform
- System design expertise
"""

cv_content = """
John Doe - Senior Software Engineer
- 6 years backend development
- Led microservices migration
- AWS certified architect
- Designed systems for 10M+ users
"""

result = agent.generate_interview_content(
    jd_content=jd_content,
    cv_content=cv_content,
    role="Senior Backend Engineer",
    level="Senior",
    round_number=2,
    num_questions=5
)
```

### Example 2: Behavioral Round for Team Lead

```python
result = agent.generate_interview_content(
    jd_file="team_lead_jd.pdf",
    cv_file="candidate_cv.pdf",
    role="Engineering Team Lead",
    level="Lead",
    round_number=3,  # Behavioral round
    num_questions=4
)
```

## 🛠️ Development

### Project Structure
```
interview_agent/
├── __init__.py                 # Package exports
├── main.py                     # Main InterviewAgent class
├── models.py                   # Data models
├── agents/                     # Specialized agents
│   ├── document_processor.py   # Document analysis
│   ├── question_generator.py   # Question generation
│   ├── answer_generator.py     # Answer generation
│   └── coordinator.py          # Workflow coordination
├── tools/                      # Utility tools
│   ├── document_parser.py      # File parsing
│   └── content_analyzer.py     # Content analysis
├── example.py                  # Usage examples
└── requirements.txt            # Dependencies
```

### Running Examples

```bash
python example.py
```

### Testing

```python
# Test with different configurations
test_cases = [
    ("Junior", 1, "Software Engineer"),
    ("Senior", 2, "Data Scientist"),
    ("Lead", 3, "Product Manager"),
    ("Principal", 4, "Engineering Director")
]

for level, round_num, role in test_cases:
    result = agent.generate_interview_content(
        jd_content=sample_jd,
        cv_content=sample_cv,
        role=role,
        level=level,
        round_number=round_num
    )
    print(f"Generated {len(result.questions)} questions for {level} {role}")
```

## 🔒 Security & Privacy

- Sanitizes sensitive information from documents
- Uses secure AWS Bedrock API calls
- No data persistence by default
- Environment variable configuration for credentials

## 📈 Performance Considerations

- **Caching**: Document processing results can be cached
- **Rate Limiting**: Built-in AWS API rate limiting
- **Token Optimization**: Efficient prompt engineering
- **Async Support**: Can be extended for async processing

## 🐛 Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   ```bash
   aws configure
   # OR
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   ```

2. **Model Access Denied**
   - Enable model access in AWS Bedrock console
   - Check IAM permissions for Bedrock

3. **File Parsing Errors**
   - Ensure file exists and is readable
   - Check file format (PDF, DOCX, TXT)
   - Verify file is not corrupted

4. **Invalid Parameters**
   ```python
   # Use validation before generation
   validation = agent.validate_inputs(role, level, round_number)
   if not validation['valid']:
       print("Errors:", validation['errors'])
   ```

### Debug Mode

```python
import logging

# Enable debug logging
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

agent = InterviewAgent()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Create an issue with detailed error information

## 🔮 Future Enhancements

- [ ] Support for more file formats (RTF, HTML)
- [ ] Integration with ATS systems
- [ ] Real-time collaboration features
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Custom question templates
- [ ] Interview scheduling integration
