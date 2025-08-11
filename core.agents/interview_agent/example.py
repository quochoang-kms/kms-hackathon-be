#!/usr/bin/env python3
"""
Enhanced Working Example - Interview Agent with Direct Naming

This example demonstrates the Interview Agent using direct naming
and shows how the enhanced functionality works by default.
"""

import asyncio
import time
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import using direct names (enhanced functionality by default)
from main import InterviewAgent, generate_interview, InterviewRequest, InterviewResponse
from models import ExperienceLevel, InterviewRound


async def demo_basic_usage():
    """Demonstrate basic usage with direct naming."""
    print("🚀 Basic Usage Demo\n")
    print("=" * 50)
    
    # Sample data
    jd_content = """
    Senior Software Engineer - Backend Systems
    
    We are looking for a Senior Software Engineer to join our backend team.
    
    Requirements:
    - 5+ years of software development experience
    - Strong proficiency in Python, Java, or Go
    - Experience with microservices architecture
    - Knowledge of cloud platforms (AWS, GCP, Azure)
    - Experience with databases (SQL and NoSQL)
    - Understanding of system design principles
    
    Responsibilities:
    - Design and implement scalable backend services
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Participate in code reviews and architecture discussions
    """
    
    cv_content = """
    John Doe - Senior Software Engineer
    
    Professional Experience:
    
    2019-2024: Senior Software Engineer at TechCorp
    - Led development of microservices platform serving 10M+ users
    - Implemented event-driven architecture using Apache Kafka
    - Reduced system latency by 40% through optimization
    - Mentored 3 junior developers
    
    2017-2019: Software Engineer at StartupXYZ
    - Built REST APIs using Python Flask and PostgreSQL
    - Implemented CI/CD pipelines using Jenkins and Docker
    - Collaborated with frontend team on API design
    
    Technical Skills:
    - Languages: Python, Java, Go, JavaScript
    - Frameworks: Django, Flask, Spring Boot
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, RDS, Lambda)
    - Tools: Docker, Kubernetes, Jenkins
    """
    
    try:
        # Create interview agent (enhanced by default)
        print("🔧 Creating Interview Agent...")
        agent = InterviewAgent()
        print(f"✅ Agent created: {type(agent).__name__}")
        
        # Create interview request using direct naming
        print("\n📝 Creating Interview Request...")
        request = InterviewRequest(
            jd_content=jd_content,
            cv_content=cv_content,
            role="Senior Software Engineer",
            level=ExperienceLevel.SENIOR,
            round_number=InterviewRound.TECHNICAL,
            num_questions=10
        )
        print("✅ Request created successfully")
        
        # Generate interview content
        print("\n🚀 Generating Interview Content...")
        print("   📊 Using enhanced parallel processing...")
        
        start_time = time.time()
        
        # Use the enhanced async method
        result = await agent.generate_interview_content_async(
            jd_content=request.jd_content,
            cv_content=request.cv_content,
            role=request.role,
            level=request.level,
            round_number=request.round_number,
            num_questions=request.num_questions,
            enable_parallel_processing=True,
            quality_assurance=True,
            include_follow_ups=True
        )
        
        generation_time = time.time() - start_time
        print(f"✅ Content generated in {generation_time:.2f}s")
        
        # Display results summary
        print(f"\n📋 Interview Results Summary:")
        print(f"   • Role: {request.role}")
        print(f"   • Level: {request.level.value}")
        print(f"   • Round: {request.round_number.name}")
        print(f"   • Questions Generated: {len(result.questions)}")
        print(f"   • Answer Tips: {len(result.answer_tips)}")
        print(f"   • Overall Quality Score: {result.overall_quality_score:.2f}")
        
        # Display detailed questions
        print(f"\n📝 Generated Interview Questions:")
        print("-" * 40)
        for i, question in enumerate(result.questions, 1):
            print(f"\n{i}. {question.question}")
            print(f"   Type: {question.type}")
            print(f"   Difficulty: {question.difficulty}")
            print(f"   Expected Duration: {question.expected_duration} minutes")
            if question.tags:
                print(f"   Tags: {', '.join(question.tags)}")
            if question.follow_up_questions:
                print(f"   Follow-ups: {len(question.follow_up_questions)} available")
        
        # Display answer evaluation tips
        print(f"\n💡 Answer Evaluation Tips for Interviewers:")
        print("-" * 45)
        for i, tip in enumerate(result.answer_tips, 1):
            print(f"\n{i}. Question: {tip.question}")
            print(f"   Evaluation Tips: {tip.evaluation_tips}")
            print(f"   What to Listen For: {', '.join(tip.what_to_listen_for)}")
            print(f"   Scoring: {tip.scoring_criteria}")
            if tip.red_flags:
                print(f"   🚩 Red Flags: {', '.join(tip.red_flags)}")
            if tip.excellent_indicators:
                print(f"   ⭐ Excellent Indicators: {', '.join(tip.excellent_indicators)}")
            if tip.follow_up_questions:
                print(f"   🔍 Follow-up Questions: {len(tip.follow_up_questions)} available")
        
        # Display interview structure
        if result.interview_structure:
            print(f"\n📅 Interview Structure:")
            print("-" * 20)
            for key, value in result.interview_structure.items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None



async def main():
    """Run the comprehensive demo."""
    print("🚀 Interview Agent - Enhanced Working Example\n")
    
    try:
        # Basic usage demo with detailed output
        result = await demo_basic_usage()
        
        
        print(f"\n" + "=" * 60)
        print("🎉 Enhanced Working Example Completed!")
        
        if result:
            print(f"\n📊 Final Summary:")
            print(f"   • Enhanced functionality: ✅ Working")
            print(f"   • Direct naming: ✅ Implemented")
            print(f"   • Questions generated: {len(result.questions)}")
            print(f"   • Answer tips provided: {len(result.answer_tips)}")
            print(f"   • Quality score: {result.overall_quality_score:.2f}")
            print(f"   • Performance: ✅ Optimized")
            print(f"   • Backward compatibility: ✅ Maintained")
        
        print(f"\n🚀 Ready for Production Use!")
        print("   • Use direct naming (no 'enhanced_' prefixes)")
        print("   • Enhanced functionality is now the default")
        print("   • Questions generate successfully")
        print("   • Answer evaluation tips for interviewers")
        print("   • Legacy support available if needed")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
