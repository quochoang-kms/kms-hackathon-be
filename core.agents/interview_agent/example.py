#!/usr/bin/env python3
"""
Example usage of the Interview Agent for generating interview questions and answers.
"""

import os
import sys

# Add the parent directory to the Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now we can import the interview_agent package
from interview_agent import InterviewAgent, generate_interview, ExperienceLevel, InterviewRound


def example_with_text_content():
    """Example using direct text content."""
    print("=== Example 1: Using Direct Text Content ===\n")
    
    # Sample job description
    jd_content = """
    Senior Software Engineer - Backend Systems
    
    We are looking for a Senior Software Engineer to join our backend team. The ideal candidate will have:
    
    Requirements:
    - 5+ years of software development experience
    - Strong proficiency in Python, Java, or Go
    - Experience with microservices architecture
    - Knowledge of cloud platforms (AWS, GCP, Azure)
    - Experience with databases (SQL and NoSQL)
    - Understanding of system design principles
    - Experience with containerization (Docker, Kubernetes)
    
    Responsibilities:
    - Design and implement scalable backend services
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Participate in code reviews and architectural decisions
    - Ensure system reliability and performance
    
    Nice to have:
    - Experience with event-driven architectures
    - Knowledge of machine learning systems
    - Open source contributions
    """
    
    # Sample CV content
    cv_content = """
    John Doe
    Senior Software Engineer
    
    Experience:
    2019-2024: Senior Software Engineer at TechCorp
    - Led development of microservices platform serving 10M+ users
    - Implemented event-driven architecture using Apache Kafka
    - Mentored 3 junior developers and conducted technical interviews
    - Reduced system latency by 40% through optimization initiatives
    
    2017-2019: Software Engineer at StartupXYZ
    - Developed REST APIs using Python Flask and PostgreSQL
    - Implemented CI/CD pipelines using Jenkins and Docker
    - Collaborated with product team on feature development
    
    Skills:
    - Programming: Python, Java, Go, JavaScript
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes
    - Tools: Git, Jenkins, Kafka, Elasticsearch
    
    Education:
    - B.S. Computer Science, University of Technology (2017)
    
    Certifications:
    - AWS Certified Solutions Architect
    - Certified Kubernetes Administrator
    """
    
    # Create agent and generate interview content
    agent = InterviewAgent()
    
    try:
        result = agent.generate_interview_content(
            jd_content=jd_content,
            cv_content=cv_content,
            role="Senior Software Engineer",
            level="Senior",
            round_number=2,  # Technical round
            num_questions=5
        )
        
        print("✅ Interview content generated successfully!\n")
        print(f"Interview Focus: {result.interview_focus}\n")
        
        print("📝 Generated Questions:")
        for i, question in enumerate(result.questions, 1):
            print(f"\n{i}. {question.question}")
            print(f"   Type: {question.type}")
            print(f"   Difficulty: {question.difficulty}")
            print(f"   Expected Duration: {question.expected_duration} minutes")
        
        print("\n💡 Sample Answers:")
        for i, answer in enumerate(result.sample_answers, 1):
            print(f"\n{i}. Question: {answer.question[:100]}...")
            print(f"   Sample Answer: {answer.answer[:200]}...")
            print(f"   Key Points: {', '.join(answer.key_points[:3])}")
        
        print(f"\n🎯 Preparation Tips:")
        for tip in result.preparation_tips:
            print(f"   • {tip}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_with_files():
    """Example using file paths (requires actual files)."""
    print("\n=== Example 2: Using File Paths ===\n")
    
    # This example assumes you have actual files
    jd_file = "sample_jd.pdf"  # Replace with actual file path
    cv_file = "sample_cv.pdf"  # Replace with actual file path
    
    if not os.path.exists(jd_file) or not os.path.exists(cv_file):
        print("⚠️  Skipping file example - sample files not found")
        print("   Create sample_jd.pdf and sample_cv.pdf to test this example")
        return
    
    try:
        result = generate_interview(
            jd_file=jd_file,
            cv_file=cv_file,
            role="Data Scientist",
            level="Mid",
            round_number=1,  # Screening round
            num_questions=4
        )
        
        print("✅ Interview content generated from files!\n")
        print(f"Interview Focus: {result.interview_focus}\n")
        
        print("📝 Generated Questions:")
        for i, question in enumerate(result.questions, 1):
            print(f"{i}. {question.question}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_different_levels_and_rounds():
    """Example showing different experience levels and interview rounds."""
    print("\n=== Example 3: Different Levels and Rounds ===\n")
    
    # Simple JD and CV for testing
    simple_jd = """
    Product Manager Position
    
    We're seeking a Product Manager to drive product strategy and execution.
    
    Requirements:
    - 3+ years product management experience
    - Strong analytical and communication skills
    - Experience with agile methodologies
    - Understanding of user research and data analysis
    """
    
    simple_cv = """
    Jane Smith - Product Manager
    
    Experience:
    2021-2024: Product Manager at GrowthCo
    - Managed product roadmap for mobile app with 1M+ users
    - Led cross-functional teams of 8 people
    - Increased user engagement by 25% through feature optimization
    
    Skills: Product strategy, User research, Data analysis, Agile, SQL
    Education: MBA, B.S. Engineering
    """
    
    # Test different combinations
    test_cases = [
        ("Junior", 1, "Junior Product Manager - Screening Round"),
        ("Mid", 2, "Mid-level Product Manager - Technical Round"),
        ("Senior", 3, "Senior Product Manager - Behavioral Round"),
        ("Lead", 4, "Lead Product Manager - Final Round")
    ]
    
    agent = InterviewAgent()
    
    for level, round_num, description in test_cases:
        print(f"\n--- {description} ---")
        
        try:
            result = agent.generate_interview_content(
                jd_content=simple_jd,
                cv_content=simple_cv,
                role="Product Manager",
                level=level,
                round_number=round_num,
                num_questions=3
            )
            
            print(f"Focus: {result.interview_focus}")
            print("Questions:")
            for i, q in enumerate(result.questions[:2], 1):  # Show first 2 questions
                print(f"  {i}. {q.question}")
                
        except Exception as e:
            print(f"❌ Error for {description}: {str(e)}")


def example_validation():
    """Example showing input validation."""
    print("\n=== Example 4: Input Validation ===\n")
    
    agent = InterviewAgent()
    
    # Test validation
    test_cases = [
        ("Software Engineer", "Senior", 2),  # Valid
        ("PM", "Invalid_Level", 2),          # Invalid level
        ("Data Scientist", "Junior", 5),     # Invalid round
        ("", "Mid", 1),                      # Invalid role
    ]
    
    for role, level, round_num in test_cases:
        validation = agent.validate_inputs(role, level, round_num)
        
        print(f"Testing: Role='{role}', Level='{level}', Round={round_num}")
        print(f"Valid: {validation['valid']}")
        if validation['errors']:
            print(f"Errors: {validation['errors']}")
        print()


def main():
    """Run all examples."""
    print("🚀 Interview Agent Examples\n")
    
    # Check if AWS credentials are configured
    if not os.environ.get('AWS_ACCESS_KEY_ID') and not os.path.exists(os.path.expanduser('~/.aws/credentials')):
        print("⚠️  Warning: AWS credentials not found. Make sure to configure AWS CLI or set environment variables.")
        print("   You can configure AWS CLI with: aws configure")
        print("   Or set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION\n")
    
    try:
        # Run examples
        example_with_text_content()
        example_with_files()
        example_different_levels_and_rounds()
        example_validation()
        
        print("\n✅ All examples completed!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
