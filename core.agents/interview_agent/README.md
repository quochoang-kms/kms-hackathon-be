# Interview Preparation Agentic System

A multi-agent system built with Strands Agents framework that helps interviewers prepare for candidate interviews by analyzing job descriptions, CVs, and generating tailored interview questions with evaluation criteria.

## Features

- **Document Processing**: Parse PDF, DOCX files or accept direct text input
- **Intelligent Analysis**: Analyze job descriptions and candidate CVs using AI
- **Skills Matching**: Compare candidate skills against job requirements
- **Question Generation**: Generate level and round-specific interview questions
- **Evaluation Criteria**: Provide expected answers and scoring rubrics
- **Multi-Level Support**: Junior, Mid, Senior, Lead, and Principal levels
- **Interview Rounds**: Screening, Technical, Behavioral, and Final rounds
- **Interview Personas**: Friendly, Serious, Analytical, Collaborative, Challenging

## Architecture

The system uses a multi-agent architecture with specialized agents:

1. **DocumentParserAgent**: Extract text from PDF/DOCX files or process direct text
2. **JDAnalyzerAgent**: Analyze job descriptions and extract requirements
3. **CVAnalyzerAgent**: Analyze candidate CVs and extract skills/experience
4. **SkillsMatcherAgent**: Match candidate skills against job requirements
5. **QuestionGeneratorAgent**: Generate interview questions based on analysis
6. **AnswerEvaluatorAgent**: Create evaluation criteria and expected answers
7. **InterviewPreparationSystem**: Main orchestrator using agent graph

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd interview_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```bash
MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0
REGION=us-west-2
AWS_PROFILE=default
LOG_LEVEL=INFO
```

## Usage

### Basic Usage

```python
import asyncio
from agents import InterviewPreparationSystem

async def main():
    system = InterviewPreparationSystem()
    
    result = await system.prepare_interview(
        jd="Software Engineer position requiring Python and React skills...",
        cv="5 years experience in full-stack development...",
        role="Software Engineer",
        level="Senior",
        round_number=2,  # Technical round
        interview_persona="Analytical"
    )
    
    print(f"Generated {result['interview_preparation']['total_questions']} questions")

asyncio.run(main())
```

### File Input Support

```python
# Using file paths
result = await system.prepare_interview(
    jd="/path/to/job_description.pdf",
    cv="/path/to/candidate_cv.docx",
    role="Data Scientist",
    level="Mid",
    round_number=1,
    interview_persona="Friendly"
)
```

### Experience Levels

- **Junior**: Focus on fundamentals, learning ability, potential
- **Mid**: Balance technical depth with practical experience
- **Senior**: Advanced concepts, leadership scenarios, architecture
- **Lead**: Team leadership, mentoring, strategic thinking
- **Principal**: Vision setting, technical strategy, organizational impact

### Interview Rounds

1. **Screening**: Basic qualifications, cultural fit, motivation
2. **Technical**: Deep technical skills, problem-solving, coding
3. **Behavioral**: STAR method, leadership, team dynamics
4. **Final**: Strategic thinking, long-term vision, final assessment

### Interview Personas

- **Friendly**: Warm, encouraging, supportive tone
- **Serious**: Professional, direct, competency-focused
- **Analytical**: Detail-oriented, probing, deep understanding
- **Collaborative**: Team-focused, partnership emphasis
- **Challenging**: Boundary-pushing, resilience testing

## Running Examples

Run the comprehensive examples:

```bash
python example.py
```

Run the main application:

```bash
python main.py
```

## Output Structure

The system returns a comprehensive analysis including:

```json
{
  "metadata": {
    "role": "Software Engineer",
    "level": "Senior",
    "round_number": 2,
    "round_name": "Technical",
    "interview_persona": "Analytical"
  },
  "analysis_results": {
    "jd_analysis": {
      "required_skills": [...],
      "preferred_skills": [...],
      "level_competencies": [...]
    },
    "cv_analysis": {
      "technical_skills": [...],
      "years_of_experience": 8,
      "leadership_experience": [...]
    },
    "skills_matching": {
      "matched_skills": [...],
      "missing_skills": [...],
      "overall_match_score": 85
    }
  },
  "interview_preparation": {
    "questions": [...],
    "total_questions": 10,
    "evaluation_criteria": [...]
  }
}
```

## Performance

- CV analysis: ~30 seconds
- Question generation: ~45 seconds
- Supports concurrent processing
- Optimized for AWS Lambda deployment

## Error Handling

The system includes comprehensive error handling for:

- Missing environment variables
- File not found errors
- Invalid input formats
- API authentication errors
- Timeout scenarios
- Invalid parameter validation

## Testing

Run unit tests:

```bash
python -m pytest tests/
```

## AWS Deployment

The system is designed for AWS Lambda deployment:

1. Package the application
2. Configure IAM roles for Bedrock access
3. Set environment variables
4. Deploy using AWS SAM or CDK

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review the example code

## Changelog

### v1.0.0
- Initial release
- Multi-agent architecture
- Support for all experience levels and interview rounds
- File and text input processing
- Comprehensive evaluation criteria