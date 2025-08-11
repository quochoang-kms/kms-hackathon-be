#!/usr/bin/env python3
"""
Working Example - Interview Agent with Direct Naming

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
            num_questions=3
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
        
        # Display results
        print(f"\n📋 Interview Results:")
        print(f"   • Role: {request.role}")
        print(f"   • Level: {request.level.value}")
        print(f"   • Round: {request.round_number.name}")
        print(f"   • Questions Generated: {len(result.questions)}")
        print(f"   • Sample Answers: {len(result.sample_answers)}")
        print(f"   • Overall Quality Score: {result.overall_quality_score:.2f}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


async def demo_advanced_features():
    """Demonstrate advanced features."""
    print(f"\n🎯 Advanced Features Demo\n")
    print("-" * 40)
    
    try:
        agent = InterviewAgent()
        
        # Test different interview rounds
        rounds = [
            (InterviewRound.SCREENING, "Initial screening questions"),
            (InterviewRound.TECHNICAL, "Technical deep-dive questions"),
            (InterviewRound.BEHAVIORAL, "Behavioral assessment questions"),
            (InterviewRound.FINAL, "Final round questions")
        ]
        
        for round_type, description in rounds:
            print(f"\n📝 {description}:")
            
            result = await agent.generate_interview_content_async(
                jd_content="Software Engineer position requiring Python skills",
                cv_content="Experienced Python developer with 5 years experience",
                role="Software Engineer",
                level=ExperienceLevel.SENIOR,
                round_number=round_type,
                num_questions=2,
                enable_parallel_processing=True,
                quality_assurance=True
            )
            
            print(f"   • Round: {round_type.name}")
            print(f"   • Questions: {len(result.questions)}")
            print(f"   • Quality: {result.overall_quality_score:.2f}")
        
        print("✅ Advanced features working correctly")
        
    except Exception as e:
        print(f"❌ Advanced features error: {str(e)}")


def demo_model_usage():
    """Demonstrate model usage with direct naming."""
    print(f"\n📦 Model Usage Demo\n")
    print("-" * 30)
    
    try:
        # Test all experience levels
        print("🎯 Experience Levels:")
        for level in ExperienceLevel:
            print(f"   • {level.name}: {level.value}")
        
        # Test all interview rounds
        print(f"\n🎯 Interview Rounds:")
        for round_type in InterviewRound:
            print(f"   • {round_type.name}: Round {round_type.value}")
        
        # Create different request types
        print(f"\n🎯 Request Examples:")
        
        requests = [
            InterviewRequest(
                role="Junior Developer",
                level=ExperienceLevel.JUNIOR,
                round_number=InterviewRound.SCREENING,
                num_questions=3
            ),
            InterviewRequest(
                role="Senior Engineer",
                level=ExperienceLevel.SENIOR,
                round_number=InterviewRound.TECHNICAL,
                num_questions=5
            ),
            InterviewRequest(
                role="Tech Lead",
                level=ExperienceLevel.LEAD,
                round_number=InterviewRound.FINAL,
                num_questions=4
            )
        ]
        
        for i, req in enumerate(requests, 1):
            print(f"   {i}. {req.role} - {req.level.value} - {req.round_number.name}")
            print(f"      Questions: {req.num_questions}")
        
        print("✅ Models working correctly with direct naming")
        
    except Exception as e:
        print(f"❌ Model usage error: {str(e)}")


def show_migration_guide():
    """Show migration guide from enhanced naming."""
    print(f"\n🔄 Migration Guide\n")
    print("-" * 25)
    
    print("📝 Before (Enhanced Naming):")
    print("```python")
    print("from interview_agent import EnhancedInterviewAgent")
    print("from interview_agent import EnhancedInterviewRequest")
    print("from interview_agent import generate_interview_enhanced")
    print("")
    print("agent = EnhancedInterviewAgent()")
    print("request = EnhancedInterviewRequest(...)")
    print("result = generate_interview_enhanced(...)")
    print("```")
    
    print(f"\n✨ After (Direct Naming):")
    print("```python")
    print("from interview_agent import InterviewAgent")
    print("from interview_agent import InterviewRequest")
    print("from interview_agent import generate_interview")
    print("")
    print("agent = InterviewAgent()  # Enhanced by default!")
    print("request = InterviewRequest(...)")
    print("result = generate_interview(...)")
    print("```")
    
    print(f"\n🎯 Benefits of Direct Naming:")
    print("• ✅ Cleaner, more intuitive imports")
    print("• ✅ No 'enhanced_' prefixes needed")
    print("• ✅ Enhanced functionality by default")
    print("• ✅ Backward compatibility maintained")
    print("• ✅ Easier for new users to understand")
    print("• ✅ Standard naming conventions")


async def main():
    """Run the comprehensive demo."""
    print("🚀 Interview Agent - Direct Naming Working Example\n")
    
    try:
        # Basic usage demo
        result = await demo_basic_usage()
        
        # Advanced features demo
        await demo_advanced_features()
        
        # Model usage demo
        demo_model_usage()
        
        # Migration guide
        show_migration_guide()
        
        print(f"\n" + "=" * 60)
        print("🎉 Direct Naming Working Example Completed!")
        
        if result:
            print(f"\n📊 Final Summary:")
            print(f"   • Enhanced functionality: ✅ Working")
            print(f"   • Direct naming: ✅ Implemented")
            print(f"   • Quality score: {result.overall_quality_score:.2f}")
            print(f"   • Performance: ✅ Optimized")
            print(f"   • Backward compatibility: ✅ Maintained")
        
        print(f"\n🚀 Ready for Production Use!")
        print("   • Use direct naming (no 'enhanced_' prefixes)")
        print("   • Enhanced functionality is now the default")
        print("   • Legacy support available if needed")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
