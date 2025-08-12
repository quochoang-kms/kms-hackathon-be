"""Example usage and demonstrations of the Interview Preparation System"""

import os
import asyncio
import time
from agents import InterviewPreparationSystem

# Set default environment variables if not present
os.environ.setdefault('MODEL_ID', 'apac.anthropic.claude-sonnet-4-20250514-v1:0')
os.environ.setdefault('REGION', 'ap-southeast-1')

# Sample data for testing
SAMPLE_JD_TEXT = """
Senior Data Scientist Position

We are seeking a Senior Data Scientist to join our AI/ML team.

Required Skills:
- 5+ years of experience in data science and machine learning
- Strong programming skills in Python and R
- Experience with ML frameworks (TensorFlow, PyTorch, Scikit-learn)
- Statistical analysis and hypothesis testing
- Data visualization and storytelling
- Experience with big data technologies (Spark, Hadoop)

Preferred Skills:
- PhD in Computer Science, Statistics, or related field
- Experience with deep learning and neural networks
- Cloud platforms (AWS, GCP, Azure)
- MLOps and model deployment
- Leadership and mentoring experience

Responsibilities:
- Lead data science projects from conception to deployment
- Mentor junior data scientists
- Collaborate with engineering teams on model implementation
- Present findings to stakeholders and executives
"""

SAMPLE_CV_TEXT = """
Dr. Emily Chen
Senior Data Scientist

Education:
- PhD in Computer Science, MIT (2018)
- MS in Statistics, Stanford University (2014)
- BS in Mathematics, UC Berkeley (2012)

Experience:
- Senior Data Scientist, DataTech Inc. (2020-Present)
  * Led ML initiatives for recommendation systems serving 10M+ users
  * Improved model accuracy by 25% using ensemble methods
  * Mentored team of 4 junior data scientists
  * Deployed models to production using MLflow and Kubernetes

- Data Scientist, AI Startup (2018-2020)
  * Built predictive models for customer churn (95% accuracy)
  * Implemented A/B testing framework
  * Developed data pipelines using Apache Spark

- Research Assistant, MIT AI Lab (2014-2018)
  * Published 8 papers in top-tier ML conferences
  * Developed novel deep learning architectures
  * Collaborated with industry partners on research projects

Skills:
- Programming: Python, R, SQL, Scala
- ML/AI: TensorFlow, PyTorch, Scikit-learn, XGBoost
- Big Data: Spark, Hadoop, Kafka
- Cloud: AWS (SageMaker, EC2, S3), GCP
- Visualization: Matplotlib, Seaborn, Tableau
- Leadership: Team management, technical mentoring
"""

async def run_comprehensive_examples():
    """Run comprehensive examples covering all scenarios"""
    print(f"Model ID: {os.getenv('MODEL_ID')}")
    print(f"Region: {os.getenv('REGION')}")
    
    system = InterviewPreparationSystem(
        model_id=os.getenv('MODEL_ID'),
        region=os.getenv('REGION')
    )
    
    # Test scenarios covering all levels, rounds, and personas
    test_scenarios = [
        # # Junior level scenarios
        # {
        #     "name": "Junior Developer - Screening (Friendly)",
        #     "level": "Junior",
        #     "round": 1,
        #     "persona": "Friendly",
        #     "jd": "Entry-level Software Developer position requiring basic programming skills in Python or Java.",
        #     "cv": "Recent CS graduate with internship experience and personal projects in web development."
        # },
        # {
        #     "name": "Junior Developer - Technical (Serious)",
        #     "level": "Junior", 
        #     "round": 2,
        #     "persona": "Serious",
        #     "jd": "Junior Software Engineer role focusing on web development and database skills.",
        #     "cv": "1 year experience as junior developer, worked on CRUD applications and basic APIs."
        # },
        
        # Mid level scenarios
        {
            "name": "Mid-level Engineer - Behavioral (Collaborative)",
            "level": "Mid",
            "round": 3,
            "persona": "Collaborative",
            "jd": "Mid-level Software Engineer with 3-5 years experience in full-stack development.",
            "cv": "4 years experience, led small projects, mentored interns, full-stack development."
        },
        
        # # Senior level scenarios
        # {
        #     "name": "Senior Data Scientist - Technical (Analytical)",
        #     "level": "Senior",
        #     "round": 2,
        #     "persona": "Analytical",
        #     "jd": SAMPLE_JD_TEXT,
        #     "cv": SAMPLE_CV_TEXT
        # },
        # {
        #     "name": "Senior Engineer - Final (Challenging)",
        #     "level": "Senior",
        #     "round": 4,
        #     "persona": "Challenging",
        #     "jd": "Senior Software Architect role requiring system design and team leadership.",
        #     "cv": "8 years experience, system architect, led teams of 10+, designed scalable systems."
        # },
        
        # # Lead level scenarios
        # {
        #     "name": "Lead Engineer - Screening (Friendly)",
        #     "level": "Lead",
        #     "round": 1,
        #     "persona": "Friendly",
        #     "jd": "Engineering Lead position managing multiple teams and technical strategy.",
        #     "cv": "10 years experience, managed 20+ engineers, drove technical vision, P&L responsibility."
        # },
        
        # # Principal level scenarios
        # {
        #     "name": "Principal Engineer - Final (Analytical)",
        #     "level": "Principal",
        #     "round": 4,
        #     "persona": "Analytical",
        #     "jd": "Principal Engineer role setting technical direction for the entire organization.",
        #     "cv": "15+ years experience, CTO at startup, technical thought leader, industry speaker."
        # }
    ]
    
    results = []
    
    print("🚀 Running Comprehensive Interview Preparation Examples")
    print("=" * 80)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📋 Scenario {i}/{len(test_scenarios)}: {scenario['name']}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            result = await system.prepare_interview(
                jd=scenario["jd"],
                cv=scenario["cv"],
                role="Software Engineer",  # Default role
                level=scenario["level"],
                round_number=scenario["round"],
                interview_persona=scenario["persona"]
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if result.get("status") == "completed":
                print(f"✅ Success! (Processing time: {processing_time:.2f}s)")
                
                # Extract key metrics
                metadata = result.get("metadata", {})
                analysis = result.get("analysis_results", {})
                interview_prep = result.get("interview_preparation", {})
                
                skills_matching = analysis.get("skills_matching", {})
                match_score = skills_matching.get("overall_match_score", 0)
                question_count = interview_prep.get("total_questions", 0)
                
                print(f"   📊 Match Score: {match_score}%")
                print(f"   ❓ Questions Generated: {question_count}")
                print(f"   🎯 Strong Areas: {len(skills_matching.get('strong_areas', []))}")
                print(f"   ⚠️  Missing Skills: {len(skills_matching.get('missing_skills', []))}")
                
                # Show sample questions
                questions = interview_prep.get("questions", [])[:2]
                if questions:
                    print(f"   📝 Sample Questions:")
                    for j, q in enumerate(questions, 1):
                        print(f"      {j}. {q.get('text', '')[:80]}...")
                        print(f"         Type: {q.get('question_type')} | Difficulty: {q.get('difficulty_level')}/5")
                
                results.append({
                    "scenario": scenario["name"],
                    "status": "success",
                    "processing_time": processing_time,
                    "match_score": match_score,
                    "question_count": question_count
                })
                
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                results.append({
                    "scenario": scenario["name"],
                    "status": "failed",
                    "error": result.get('error', 'Unknown error')
                })
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            results.append({
                "scenario": scenario["name"],
                "status": "exception",
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 EXECUTION SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    
    print(f"✅ Successful scenarios: {len(successful)}/{len(results)}")
    print(f"❌ Failed scenarios: {len(failed)}/{len(results)}")
    
    if successful:
        avg_time = sum(r["processing_time"] for r in successful) / len(successful)
        avg_match_score = sum(r["match_score"] for r in successful) / len(successful)
        avg_questions = sum(r["question_count"] for r in successful) / len(successful)
        
        print(f"\n📈 Performance Metrics (Successful scenarios):")
        print(f"   ⏱️  Average Processing Time: {avg_time:.2f}s")
        print(f"   🎯 Average Match Score: {avg_match_score:.1f}%")
        print(f"   ❓ Average Questions Generated: {avg_questions:.1f}")
    
    if failed:
        print(f"\n❌ Failed Scenarios:")
        for result in failed:
            print(f"   - {result['scenario']}: {result.get('error', 'Unknown error')}")
    
    return results

async def run_file_input_examples():
    """Demonstrate file input capabilities"""
    print("\n" + "=" * 80)
    print("📁 FILE INPUT EXAMPLES")
    print("=" * 80)
    
    # Create sample files for testing
    sample_files_dir = "./sample_files"
    os.makedirs(sample_files_dir, exist_ok=True)
    
    # Create sample JD file
    jd_file_path = os.path.join(sample_files_dir, "sample_jd.txt")
    with open(jd_file_path, "w") as f:
        f.write(SAMPLE_JD_TEXT)
    
    # Create sample CV file
    cv_file_path = os.path.join(sample_files_dir, "sample_cv.txt")
    with open(cv_file_path, "w") as f:
        f.write(SAMPLE_CV_TEXT)
    
    print(f"📄 Created sample files:")
    print(f"   - JD: {jd_file_path}")
    print(f"   - CV: {cv_file_path}")
    
    # Test file input
    system = InterviewPreparationSystem(
        model_id=os.getenv('MODEL_ID'),
        region=os.getenv('REGION')
    )
    
    print(f"\n🔄 Testing file input processing...")
    
    try:
        result = await system.prepare_interview(
            jd=jd_file_path,  # File path input
            cv=cv_file_path,  # File path input
            role="Data Scientist",
            level="Senior",
            round_number=2,
            interview_persona="Analytical"
        )
        
        if result.get("status") == "completed":
            print("✅ File input processing successful!")
            
            # Show parsing metadata
            analysis = result.get("analysis_results", {})
            print(f"   📊 JD Skills Identified: {len(analysis.get('jd_analysis', {}).get('required_skills', []))}")
            print(f"   📊 CV Skills Identified: {len(analysis.get('cv_analysis', {}).get('technical_skills', []))}")
            
        else:
            print(f"❌ File input processing failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ File input test failed: {str(e)}")
    
    # Cleanup
    try:
        os.remove(jd_file_path)
        os.remove(cv_file_path)
        os.rmdir(sample_files_dir)
        print(f"🧹 Cleaned up sample files")
    except:
        pass

async def performance_benchmark():
    """Run performance benchmarks"""
    print("\n" + "=" * 80)
    print("⚡ PERFORMANCE BENCHMARK")
    print("=" * 80)
    
    system = InterviewPreparationSystem(
        model_id=os.getenv('MODEL_ID'),
        region=os.getenv('REGION')
    )
    
    # Simple benchmark scenario
    benchmark_jd = "Software Engineer position requiring Python, JavaScript, and database skills."
    benchmark_cv = "3 years experience in full-stack development with Python, React, and PostgreSQL."
    
    times = []
    
    print("🏃 Running 3 benchmark iterations...")
    
    for i in range(3):
        print(f"   Iteration {i+1}/3...", end=" ")
        
        start_time = time.time()
        
        try:
            result = await system.prepare_interview(
                jd=benchmark_jd,
                cv=benchmark_cv,
                role="Software Engineer",
                level="Mid",
                round_number=2,
                interview_persona="Friendly"
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            times.append(processing_time)
            
            if result.get("status") == "completed":
                print(f"✅ {processing_time:.2f}s")
            else:
                print(f"❌ Failed")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📊 Benchmark Results:")
        print(f"   ⏱️  Average Time: {avg_time:.2f}s")
        print(f"   🚀 Fastest Time: {min_time:.2f}s")
        print(f"   🐌 Slowest Time: {max_time:.2f}s")
        
        # Performance assessment
        if avg_time <= 30:
            print("   🎯 Performance: Excellent (≤30s)")
        elif avg_time <= 45:
            print("   ⚠️  Performance: Good (≤45s)")
        else:
            print("   🔴 Performance: Needs improvement (>45s)")

async def main():
    """Main example function"""
    print("🎯 Interview Preparation System - Comprehensive Examples")
    print("=" * 80)
    
    # Check environment
    if not os.getenv('MODEL_ID') or not os.getenv('REGION'):
        print("❌ Missing environment variables. Please set MODEL_ID and REGION in .env file")
        return
    
    try:
        # Run comprehensive examples
        await run_comprehensive_examples()
        
        # Run file input examples
        await run_file_input_examples()
        
        # Run performance benchmark
        # await performance_benchmark()
        
        print("\n" + "=" * 80)
        print("🎉 All examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Examples failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())