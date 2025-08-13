## Code Generation Prompt for Interview Preparation Agentic System

Context & Requirements:
• Programming language: Python 3.8+
• Framework/libraries: strands-agents, strands-agents-tools, boto3, PyPDF2/pdfplumber, python-docx, python-dotenv
• Environment: AWS Lambda/Local development
• Model: Amazon Bedrock (Claude 3.7 Sonnet or similar)
• Architecture: Strands Agents with Agent Graph multi-agent architecture

Project Structure:
interview_agent/
├── agents/                 # Folder containing all agent implementations
│   ├── __init__.py
│   ├── document_parser.py  # Document parsing agent
│   ├── jd_analyzer.py      # Job description analyzer agent
│   ├── cv_analyzer.py      # CV analyzer agent
│   ├── skills_matcher.py   # Skills matching agent
│   ├── question_generator.py # Question generation agent
│   ├── answer_evaluator.py # Answer evaluation agent
│   └── interview_system.py # Main orchestrator agent graph
├── main.py                 # Main application entry point
├── example.py              # Example usage and demonstrations
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .env                   # Environment variables (MODEL_ID, REGION)


Task Description:
Create a multi-agent system using Strands Agents framework that helps interviewers prepare for candidate interviews by analyzing job descriptions, CVs, and generating tailored interview questions with expected
answers and evaluation criteria.

Functional Requirements:
• Parse and extract text from PDF and DOCX files (CV documents) OR accept direct text input
• Accept job descriptions as direct text strings OR file paths
• Analyze job descriptions and candidate CVs to identify key skills
• Match candidate skills against job requirements
• Identify skill gaps and potential red flags
• Generate role-appropriate interview questions based on level and round
• Provide expected answers with evaluation criteria and scoring guides
• Support different interview personas and question types
• Handle multiple interview rounds with progressive difficulty
• **Implement experience level-specific question generation and evaluation**
• **Support structured interview round progression**
• **Generate questions based on specific question types and interview personas**

Technical Constraints:
• Must use async/await patterns for file processing
• Handle large PDF/DOCX files efficiently (up to 10MB)
• Process multiple documents concurrently
• Support both file input and direct text input seamlessly
• Implement comprehensive error handling for file parsing and text validation
• Follow AWS Lambda best practices if deployed to AWS
• Maintain conversation context across agent interactions
• Load configuration from .env file

Input/Output Specifications:
• Input:
  • JD (string text OR file path)
  • CV (string text OR PDF/DOCX file path OR binary data)
  • Role (string: e.g., "Software Engineer", "Data Scientist")
  • **Level (string: "Junior", "Mid", "Senior", "Lead", "Principal")**
  • **Round Number (int: 1-4 corresponding to Screening, Technical, Behavioral, Final)**
  • **Interview Persona (string: "Friendly", "Serious", or custom persona)**

• Output:
  • Analyzer Results:
    • Key skills from JD (list)
    • Key skills from CV (list)
    • Matched skills (list with confidence scores)
    • Missing skills (list with criticality levels)
    • Potential red flags (list with descriptions)
    • Strong areas (list with evidence)

  • Question Set:
    • **Questions (list of objects with: text, question_type, difficulty_level, round_alignment, persona_style)**
    • **Expected answers (key points, evaluation criteria, scoring guide 1-5, level_expectations)**

Experience Level Guidelines:
EXPERIENCE LEVELS:
- Junior: Focus on fundamentals, learning ability, potential, basic technical concepts
- Mid: Balance of technical depth and practical experience, problem-solving scenarios
- Senior: Advanced technical concepts, leadership scenarios, architectural decisions
- Lead: Team leadership, mentoring, strategic thinking, cross-functional collaboration
- Principal: Vision setting, technical strategy, organizational impact, industry expertise

INTERVIEW ROUNDS:
- Round 1 (Screening): Basic qualifications, cultural fit, motivation, overview of experience
- Round 2 (Technical): Deep technical skills, problem-solving, coding/design challenges
- Round 3 (Behavioral): Past experiences, leadership, teamwork, conflict resolution
- Round 4 (Final): Strategic thinking, long-term vision, final cultural assessment

QUESTION TYPES:
- Technical: Specific to role requirements, coding, system design, tools, methodologies
- Behavioral: Past experiences using STAR method, soft skills, team dynamics
- Situational: Hypothetical scenarios, problem-solving approach, decision-making
- Cultural Fit: Values alignment, work style, company culture match

INTERVIEW PERSONAS:
- Friendly: Warm, encouraging, supportive tone, puts candidate at ease
- Serious: Professional, direct, focused on competency assessment
- Analytical: Detail-oriented, probing, seeks deep understanding
- Collaborative: Team-focused, emphasizes partnership and cooperation
- Challenging: Pushes boundaries, tests resilience and problem-solving under pressure


File-Specific Implementation Requirements:

agents/init__.py:**
• Export all agent classes and main system class
• Provide convenient imports for the package
• **Export experience level and round configuration constants**

agents/document_parser.py:
• Implement DocumentParserAgent class
• Handle PDF and DOCX parsing with error handling
• Support direct text input validation and processing
• Implement input type detection (text vs file path vs binary)
• Extract clean text and metadata from documents
• Use @tool decorator for parsing functions
• Add text preprocessing and cleaning for direct text inputs

agents/jd_analyzer.py:
• Implement JDAnalyzerAgent class
• Accept both text strings and parsed document content
• Parse job descriptions and extract key requirements
• Identify required vs preferred skills
• Categorize skills by type (technical, soft skills, etc.)
• Handle various JD formats (structured, unstructured text)
• **Extract role-specific competency requirements**
• **Identify level-appropriate skill expectations**

agents/cv_analyzer.py:
• Implement CVAnalyzerAgent class
• Accept both text strings and parsed document content
• Analyze candidate background, experience, and skills
• Extract education, work history, and achievements
• Identify skill levels and proficiency indicators
• Handle various CV formats (structured, unstructured text)
• **Assess candidate's experience level alignment**
• **Identify leadership and mentoring experience for senior levels**

agents/skills_matcher.py:
• Implement SkillsMatcherAgent class
• Compare JD requirements against CV skills
• Calculate match scores and identify gaps
• Flag potential concerns or strong areas
• **Provide level-specific skill gap analysis**
• **Assess readiness for target experience level**

agents/question_generator.py:
• Implement QuestionGeneratorAgent class
• **Generate questions based on experience level guidelines**
• **Adapt questions to specific interview rounds**
• **Apply interview persona styling to questions**
• **Ensure question type alignment (Technical, Behavioral, Situational, Cultural Fit)**
• Generate questions based on role, level, and round
• Ensure progressive difficulty across rounds
• **Implement level-specific question complexity scaling**

agents/answer_evaluator.py:
• Implement AnswerEvaluatorAgent class
• Create expected answer frameworks
• **Define level-specific evaluation criteria and scoring rubrics**
• **Provide experience level-appropriate assessment guidelines**
• Provide interviewer guidance for assessment
• **Include persona-specific evaluation approaches**
• **Generate STAR method evaluation criteria for behavioral questions**

agents/interview_system.py:
• Implement InterviewPreparationSystem class using agent_graph
• Orchestrate the workflow between all agents
• Handle input type detection and routing
• Manage state and data flow
• Handle error recovery and fallbacks
• Implement flexible input processing pipeline
• **Coordinate level and round-specific processing**
• **Manage persona consistency across all agents**

main.py:
• Main application entry point
• Load environment variables from .env
• Initialize and run the interview preparation system
• Handle command-line arguments if needed
• Support both file and text input modes
• **Include validation for experience levels and round numbers**

example.py:
• Demonstrate complete workflow with sample data
• Show examples with both file inputs and direct text inputs
• **Show different experience level scenarios**
• **Demonstrate all interview rounds and question types**
• **Include examples for different interview personas**
• Show different use cases and configurations
• Include performance benchmarking
• Provide testing scenarios
• Include sample JD and CV text for testing

requirements.txt:
strands-agents>=0.1.0
strands-agents-tools>=0.1.0
boto3>=1.26.0
PyPDF2>=3.0.0
pdfplumber>=0.9.0
python-docx>=0.8.11
python-dotenv>=1.0.0
asyncio>=3.4.3
typing-extensions>=4.0.0


.env file structure:
MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0
REGION=us-west-2
AWS_PROFILE=default
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=5
TIMEOUT_SECONDS=60


Agent Architecture Design:
• Use Agent Graph architecture with the following specialized agents:
  1. **DocumentParserAgent**: Extract and clean text from CV files OR process direct text input
  2. **JDAnalyzerAgent**: Parse job description and extract requirements from text or files
  3. **CVAnalyzerAgent**: Analyze candidate background and skills from text or files
  4. **SkillsMatcherAgent**: Compare JD vs CV and identify gaps with level-specific analysis
  5. **QuestionGeneratorAgent**: Create interview questions based on analysis, level, round, and persona
  6. **AnswerEvaluatorAgent**: Generate expected answers and level-appropriate scoring criteria

Code Style Preferences:
• Use async/await patterns throughout
• Include comprehensive error handling with specific exception types
• Follow PEP 8 style guidelines
• Include detailed docstrings with parameter and return type documentation
• Use type hints for all functions and methods
• Implement logging for debugging and monitoring
• Follow AWS Lambda best practices for resource management
• Load configuration from environment variables using python-dotenv

Additional Requirements:
• Include unit tests: yes (test each agent independently and integration tests)
• Test both file input and direct text input scenarios
• **Test all experience levels and interview rounds**
• **Test different question types and interview personas**
• Include example usage: yes (complete workflow example in example.py)
• Include documentation: yes (comprehensive README.md)
• Follow AWS best practices: yes
• Include configuration management for different models and parameters
• Implement retry logic for LLM API calls
• Add validation for input parameters
• Environment variable validation and error handling
• Input type validation and sanitization

Specific Implementation Details:
• Create custom tools for document parsing using @tool decorator
• Implement input type detection utility functions
• Implement agent graph with clear dependencies between agents
• Use journal tool for maintaining state across agent interactions
• Include callback handlers for progress tracking
• Implement streaming responses for real-time feedback
• Add configuration for different Bedrock models from .env
• Include prompt templates for each specialized agent
• Implement caching mechanism for repeated CV analysis
• Proper module imports and package structure
• Add text preprocessing utilities for direct text inputs
• **Implement experience level and round validation utilities**
• **Create persona-specific prompt templates**
• **Add question type classification and validation**

Example Usage in main.py:
python
import os
import asyncio
from dotenv import load_dotenv
from agents import InterviewPreparationSystem

async def main():
    # Load environment variables
    load_dotenv()

    # Initialize system with env config
    system = InterviewPreparationSystem(
        model_id=os.getenv('MODEL_ID'),
        region=os.getenv('REGION')
    )

    # Example 1: Junior level screening round with friendly persona
    result_junior = await system.prepare_interview(
        jd="Software Engineer Position - Entry Level",
        cv="Recent graduate with internship experience...",
        role="Software Engineer",
        level="Junior",  # Focus on fundamentals and potential
        round_number=1,  # Screening round
        interview_persona="Friendly"  # Encouraging approach
    )

    # Example 2: Senior level technical round with analytical persona
    result_senior = await system.prepare_interview(
        jd="Senior Software Engineer - System Architecture",
        cv="8 years experience, team lead, system design...",
        role="Software Engineer",
        level="Senior",  # Advanced technical concepts
        round_number=2,  # Technical deep dive
        interview_persona="Analytical"  # Detail-oriented assessment
    )

    # Example 3: Principal level final round with collaborative persona
    result_principal = await system.prepare_interview(
        jd="Principal Engineer - Technical Strategy",
        cv="15+ years, technical leadership, vision setting...",
        role="Software Engineer",
        level="Principal",  # Vision and strategy focus
        round_number=4,  # Final assessment
        interview_persona="Collaborative"  # Partnership evaluation
    )

    print("Analysis complete for all levels!")
    return result_junior, result_senior, result_principal

if __name__ == "__main__":
    asyncio.run(main())


Level-Specific Processing Requirements:
• **Junior Level**: Generate questions focusing on learning ability, basic concepts, potential for growth
• **Mid Level**: Balance technical depth with practical experience, include problem-solving scenarios
• **Senior Level**: Emphasize advanced technical concepts, leadership scenarios, architectural thinking
• **Lead Level**: Focus on team leadership, mentoring capabilities, strategic thinking, collaboration
• **Principal Level**: Assess vision setting, technical strategy, organizational impact, industry expertise

Round-Specific Processing Requirements:
• **Round 1 (Screening)**: Basic qualifications, cultural fit, motivation assessment
• **Round 2 (Technical)**: Deep technical evaluation, problem-solving, hands-on challenges
• **Round 3 (Behavioral)**: STAR method questions, leadership examples, team dynamics
• **Round 4 (Final)**: Strategic thinking, long-term vision, comprehensive cultural assessment

Question Type Implementation:
• **Technical Questions**: Role-specific, coding challenges, system design, methodology assessment
• **Behavioral Questions**: STAR method structure, past experience analysis, soft skills evaluation
• **Situational Questions**: Hypothetical scenarios, decision-making process, problem-solving approach
• **Cultural Fit Questions**: Values alignment, work style compatibility, company culture match

Interview Persona Implementation:
• **Friendly**: Warm tone, encouraging language, supportive questioning style
• **Serious**: Professional approach, direct questions, competency-focused assessment
• **Analytical**: Detail-oriented questions, probing follow-ups, deep understanding focus
• **Collaborative**: Team-oriented questions, partnership emphasis, cooperation assessment
• **Challenging**: Boundary-pushing questions, resilience testing, pressure scenario evaluation

Error Handling Requirements:
• Handle missing environment variables gracefully
• Implement file not found error handling
• Handle invalid text input formats
• Validate text content quality and completeness
• **Validate experience level and round number inputs**
• **Handle invalid interview persona specifications**
• Handle Bedrock API authentication and authorization errors
• Validate input parameters with clear error messages
• Log all errors with context for debugging
• Provide fallback responses when agents fail
• Handle timeout scenarios for long-running operations

Performance Requirements:
• Process CV analysis within 30 seconds
• Generate question sets within 45 seconds
• Optimize text processing for direct inputs
• Support concurrent processing of multiple requests
• Optimize memory usage for large document processing
• Implement connection pooling for Bedrock API calls
• Cache parsed documents to avoid re-processing
• Cache processed text inputs for repeated analysis
• **Optimize level and round-specific processing for performance**