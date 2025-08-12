"""Main application entry point for Interview Preparation System"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from agents import InterviewPreparationSystem, EXPERIENCE_LEVELS, INTERVIEW_ROUNDS, INTERVIEW_PERSONAS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main application function"""
    # Load environment variables
    load_dotenv()
    
    # Validate environment variables
    model_id = os.getenv('MODEL_ID')
    region = os.getenv('REGION')
    
    if not model_id or not region:
        logger.error("Missing required environment variables: MODEL_ID and REGION")
        return
    
    logger.info(f"Initializing Interview Preparation System with model: {model_id}")
    
    # Initialize system
    system = InterviewPreparationSystem(
        model_id=model_id,
        region=region
    )
    
    # Example usage scenarios
    scenarios = [
        {
            "name": "Junior Software Engineer - Screening Round",
            "jd": """
            Software Engineer - Entry Level Position
            
            We are looking for a Junior Software Engineer to join our development team.
            
            Required Skills:
            - Programming fundamentals in Python or Java
            - Basic understanding of data structures and algorithms
            - Familiarity with version control (Git)
            - Basic web development concepts
            
            Preferred Skills:
            - Experience with databases (SQL)
            - Understanding of software testing
            - Agile development experience
            
            This is an excellent opportunity for a recent graduate or someone with 1-2 years of experience.
            """,
            "cv": """
            John Smith
            Recent Computer Science Graduate
            
            Education:
            - BS Computer Science, State University (2023)
            - GPA: 3.7/4.0
            
            Experience:
            - Software Development Intern, Tech Startup (Summer 2022)
              * Developed web applications using Python and Flask
              * Worked with PostgreSQL database
              * Participated in Agile sprints
            
            Projects:
            - Personal Portfolio Website (React, Node.js)
            - Data Analysis Tool (Python, Pandas)
            - Mobile App Prototype (React Native)
            
            Skills:
            - Programming: Python, Java, JavaScript
            - Web: HTML, CSS, React, Flask
            - Database: SQL, PostgreSQL
            - Tools: Git, VS Code, Docker
            """,
            "role": "Software Engineer",
            "level": "Junior",
            "round_number": 1,
            "persona": "Friendly"
        },
        {
            "name": "Senior Software Engineer - Technical Round",
            "jd": """
            Senior Software Engineer - System Architecture
            
            We need an experienced Senior Software Engineer to lead technical initiatives.
            
            Required Skills:
            - 5+ years of software development experience
            - Strong system design and architecture skills
            - Experience with microservices and distributed systems
            - Leadership and mentoring experience
            - Cloud platforms (AWS, Azure, or GCP)
            
            Preferred Skills:
            - Container orchestration (Kubernetes)
            - DevOps practices and CI/CD
            - Performance optimization
            - Technical writing and documentation
            """,
            "cv": """
            Sarah Johnson
            Senior Software Engineer
            
            Experience:
            - Senior Software Engineer, TechCorp (2019-Present)
              * Led development of microservices architecture serving 1M+ users
              * Mentored 3 junior developers
              * Designed and implemented CI/CD pipelines
              * Reduced system latency by 40% through optimization
            
            - Software Engineer, StartupXYZ (2016-2019)
              * Built scalable web applications using Node.js and React
              * Implemented automated testing frameworks
              * Collaborated with cross-functional teams
            
            Skills:
            - Languages: JavaScript, Python, Go, Java
            - Cloud: AWS (EC2, S3, Lambda, RDS)
            - Architecture: Microservices, REST APIs, GraphQL
            - DevOps: Docker, Kubernetes, Jenkins, Terraform
            - Leadership: Team mentoring, technical decision making
            """,
            "role": "Software Engineer",
            "level": "Senior",
            "round_number": 2,
            "persona": "Analytical"
        }
    ]
    
    # Run scenarios
    for scenario in scenarios:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running scenario: {scenario['name']}")
        logger.info(f"{'='*60}")
        
        try:
            result = await system.prepare_interview(
                jd=scenario["jd"],
                cv=scenario["cv"],
                role=scenario["role"],
                level=scenario["level"],
                round_number=scenario["round_number"],
                interview_persona=scenario["persona"]
            )
            
            if result.get("status") == "completed":
                logger.info("✅ Interview preparation completed successfully!")
                
                # Print summary
                metadata = result.get("metadata", {})
                analysis = result.get("analysis_results", {})
                interview_prep = result.get("interview_preparation", {})
                
                print(f"\n📋 INTERVIEW PREPARATION SUMMARY")
                print(f"Role: {metadata.get('role')} ({metadata.get('level')} level)")
                print(f"Round: {metadata.get('round_number')} - {metadata.get('round_name')}")
                print(f"Persona: {metadata.get('interview_persona')}")
                
                print(f"\n🎯 SKILLS ANALYSIS")
                skills_matching = analysis.get("skills_matching", {})
                print(f"Overall Match Score: {skills_matching.get('overall_match_score', 0)}%")
                print(f"Strong Areas: {len(skills_matching.get('strong_areas', []))}")
                print(f"Missing Skills: {len(skills_matching.get('missing_skills', []))}")
                
                print(f"\n❓ INTERVIEW QUESTIONS")
                print(f"Total Questions Generated: {interview_prep.get('total_questions', 0)}")
                
                # Show first few questions
                questions = interview_prep.get("questions", [])[:3]
                for i, q in enumerate(questions, 1):
                    print(f"{i}. {q.get('text', '')}")
                    print(f"   Type: {q.get('question_type', 'N/A')} | Difficulty: {q.get('difficulty_level', 'N/A')}/5")
                
                if len(interview_prep.get("questions", [])) > 3:
                    print(f"   ... and {len(interview_prep.get('questions', [])) - 3} more questions")
                
            else:
                logger.error(f"❌ Interview preparation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Scenario failed: {str(e)}")
    
    logger.info(f"\n{'='*60}")
    logger.info("All scenarios completed!")
    logger.info(f"{'='*60}")

def validate_environment():
    """Validate required environment variables"""
    required_vars = ['MODEL_ID', 'REGION']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following in your .env file:")
        print("MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0")
        print("REGION=us-west-2")
        print("AWS_PROFILE=default")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Interview Preparation System...")
    
    if not validate_environment():
        exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Interview Preparation System stopped by user")
    except Exception as e:
        logger.error(f"❌ Application failed: {str(e)}")
        exit(1)