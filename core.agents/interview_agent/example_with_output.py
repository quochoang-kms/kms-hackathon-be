"""Example usage with output saved to file"""

import os
import asyncio
import time
import json
from datetime import datetime
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

class OutputSaver:
    """Helper class to save outputs to files"""
    
    def __init__(self, output_dir="./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_json(self, data, filename):
        """Save data as JSON file"""
        filepath = os.path.join(self.output_dir, f"{self.timestamp}_{filename}")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath
    
    def save_text(self, text, filename):
        """Save text to file"""
        filepath = os.path.join(self.output_dir, f"{self.timestamp}_{filename}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return filepath

async def run_single_example_with_output():
    """Run a single example and save all outputs"""
    print("🎯 Interview Preparation System - Single Example with Output")
    print("=" * 80)
    
    # Initialize output saver
    output_saver = OutputSaver()
    
    # Initialize system
    system = InterviewPreparationSystem(
        model_id=os.getenv('MODEL_ID'),
        region=os.getenv('REGION')
    )
    
    # Test scenario
    scenario = {
        "name": "Senior Data Scientist - Technical Round",
        "level": "Senior",
        "round": 2,
        "persona": "Analytical",
        "jd": SAMPLE_JD_TEXT,
        "cv": SAMPLE_CV_TEXT
    }
    
    print(f"📋 Running Scenario: {scenario['name']}")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        result = await system.prepare_interview(
            jd=scenario["jd"],
            cv=scenario["cv"],
            role="Data Scientist",
            level=scenario["level"],
            round_number=scenario["round"],
            interview_persona=scenario["persona"]
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if result.get("status") == "completed":
            print(f"✅ Success! (Processing time: {processing_time:.2f}s)")
            
            # Save complete result to JSON
            json_file = output_saver.save_json(result, "interview_preparation_result.json")
            print(f"💾 Complete result saved to: {json_file}")
            
            # Extract and save individual components
            metadata = result.get("metadata", {})
            analysis = result.get("analysis_results", {})
            interview_prep = result.get("interview_preparation", {})
            
            # Save metadata
            metadata_file = output_saver.save_json(metadata, "metadata.json")
            print(f"💾 Metadata saved to: {metadata_file}")
            
            # Save analysis results
            analysis_file = output_saver.save_json(analysis, "analysis_results.json")
            print(f"💾 Analysis results saved to: {analysis_file}")
            
            # Save interview questions
            questions_file = output_saver.save_json(interview_prep, "interview_questions.json")
            print(f"💾 Interview questions saved to: {questions_file}")
            
            # Create a human-readable summary
            summary = create_readable_summary(result, processing_time)
            summary_file = output_saver.save_text(summary, "summary.txt")
            print(f"💾 Human-readable summary saved to: {summary_file}")
            
            # Print key metrics
            skills_matching = analysis.get("skills_matching", {})
            match_score = skills_matching.get("overall_match_score", 0)
            question_count = interview_prep.get("total_questions", 0)
            
            print(f"\n📊 Key Metrics:")
            print(f"   🎯 Match Score: {match_score}%")
            print(f"   ❓ Questions Generated: {question_count}")
            print(f"   💪 Strong Areas: {len(skills_matching.get('strong_areas', []))}")
            print(f"   ⚠️  Missing Skills: {len(skills_matching.get('missing_skills', []))}")
            
            # Show sample questions
            questions = interview_prep.get("questions", [])[:3]
            if questions:
                print(f"\n📝 Sample Questions:")
                for i, q in enumerate(questions, 1):
                    print(f"   {i}. {q.get('text', '')}")
                    print(f"      Type: {q.get('question_type')} | Difficulty: {q.get('difficulty_level', 'N/A')}/5")
            
            return result
            
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            # Save error result too
            error_file = output_saver.save_json(result, "error_result.json")
            print(f"💾 Error result saved to: {error_file}")
            return result
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        error_data = {
            "error": str(e),
            "scenario": scenario,
            "timestamp": datetime.now().isoformat()
        }
        error_file = output_saver.save_json(error_data, "exception_error.json")
        print(f"💾 Exception details saved to: {error_file}")
        return None

def create_readable_summary(result, processing_time):
    """Create a human-readable summary of the interview preparation results"""
    
    metadata = result.get("metadata", {})
    analysis = result.get("analysis_results", {})
    interview_prep = result.get("interview_preparation", {})
    
    summary = f"""
      INTERVIEW PREPARATION SUMMARY
      {"=" * 50}

      SCENARIO DETAILS:
      Role: {metadata.get('role', 'N/A')}
      Level: {metadata.get('level', 'N/A')}
      Round: {metadata.get('round_number', 'N/A')} - {metadata.get('round_name', 'N/A')}
      Interview Persona: {metadata.get('interview_persona', 'N/A')}
      Processing Time: {processing_time:.2f} seconds
      Timestamp: {metadata.get('timestamp', 'N/A')}

      JOB DESCRIPTION ANALYSIS:
      {"=" * 30}
      Required Skills ({len(analysis.get('jd_analysis', {}).get('required_skills', []))} items):
      """
    
    # Add required skills
    for skill in analysis.get('jd_analysis', {}).get('required_skills', []):
        summary += f"  • {skill}\n"
    
    summary += f"\nPreferred Skills ({len(analysis.get('jd_analysis', {}).get('preferred_skills', []))} items):\n"
    for skill in analysis.get('jd_analysis', {}).get('preferred_skills', []):
        summary += f"  • {skill}\n"
    
    summary += f"""
      CV ANALYSIS:
      {"=" * 15}
      Years of Experience: {analysis.get('cv_analysis', {}).get('years_of_experience', 'N/A')}
      Technical Skills ({len(analysis.get('cv_analysis', {}).get('technical_skills', []))} items):
      """
    
    # Add technical skills
    for skill in analysis.get('cv_analysis', {}).get('technical_skills', [])[:10]:  # Limit to first 10
        summary += f"  • {skill}\n"
    
    if len(analysis.get('cv_analysis', {}).get('technical_skills', [])) > 10:
        summary += f"  ... and {len(analysis.get('cv_analysis', {}).get('technical_skills', [])) - 10} more\n"
    
    skills_matching = analysis.get('skills_matching', {})
    summary += f"""
      SKILLS MATCHING:
      {"=" * 20}
      Overall Match Score: {skills_matching.get('overall_match_score', 0)}%

      Strong Areas ({len(skills_matching.get('strong_areas', []))} items):
      """
    
    for area in skills_matching.get('strong_areas', []):
        summary += f"  ✅ {area}\n"
    
    summary += f"\nMissing Skills ({len(skills_matching.get('missing_skills', []))} items):\n"
    for skill in skills_matching.get('missing_skills', []):
        summary += f"  ❌ {skill}\n"
    
    summary += f"""
      INTERVIEW QUESTIONS:
      {"=" * 25}
      Total Questions Generated: {interview_prep.get('total_questions', 0)}

      Questions:
      """
          
    # Add all questions
    for i, question in enumerate(interview_prep.get('questions', []), 1):
        summary += f"\n{i}. {question.get('text', '')}\n"
        summary += f"   Type: {question.get('question_type', 'N/A')}\n"
        summary += f"   Difficulty: {question.get('difficulty_level', 'N/A')}/5\n"
        summary += f"   Round Alignment: {question.get('round_alignment', 'N/A')}\n"
        
        # Add expected answer points if available
        evaluation = next((e for e in interview_prep.get('evaluation_criteria', []) 
                          if e.get('question_id') == i), None)
        if evaluation and evaluation.get('expected_answer_points'):
            summary += f"   Expected Answer Points:\n"
            for point in evaluation.get('expected_answer_points', [])[:3]:  # First 3 points
                summary += f"     • {point}\n"
    
    summary += f"""
      EVALUATION CRITERIA:
      {"=" * 25}
      Total Evaluation Criteria: {len(interview_prep.get('evaluation_criteria', []))}

      The system has generated detailed evaluation criteria for each question including:
      - Expected answer points
      - Scoring rubrics (1-5 scale)
      - Level-specific expectations
      - Red flags to watch for
      - Follow-up questions
      - STAR method criteria (for behavioral questions)
      - Persona-specific evaluation approaches

      END OF SUMMARY
      {"=" * 50}
      """
    
    return summary

async def main():
    """Main function"""
    print("🎯 Interview Preparation System - Example with File Output")
    print("=" * 80)
    
    # Check environment
    if not os.getenv('MODEL_ID') or not os.getenv('REGION'):
        print("❌ Missing environment variables. Please set MODEL_ID and REGION in .env file")
        return
    
    try:
        result = await run_single_example_with_output()
        
        if result and result.get("status") == "completed":
            print("\n" + "=" * 80)
            print("🎉 Example completed successfully!")
            print("📁 Check the './output' directory for saved files")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("❌ Example completed with issues")
            print("📁 Check the './output' directory for error details")
            print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Example failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
