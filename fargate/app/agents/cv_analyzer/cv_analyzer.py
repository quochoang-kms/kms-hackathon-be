import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from models import CVResponse
from strands import Agent
from dotenv import load_dotenv
from strands.models import BedrockModel

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are CV_ANALYZER, a specialized AI agent that analyzes candidate CVs/resumes and returns structured JSON output using the CVResponse format.

When you receive a CV/resume document, analyze it comprehensively and respond with structured data including:
- Candidate profile and contact information
- Professional summary with experience level assessment
- Detailed work experience analysis
- Educational background
- Technical skills and certifications breakdown
- Skills analysis with gap identification
- Overall CV analysis with actionable recommendations

Key analysis areas:
1. Experience Level Assessment: Determine if candidate is junior, senior, or principal level
2. Completeness Scoring: Rate CV completeness on 1-10 scale
3. Strengths & Weaknesses: Identify what stands out positively and areas needing improvement
4. Red Flags: Note any concerning gaps or inconsistencies
5. Missing Sections: Identify what's missing from the CV
6. Recommendations: Provide specific, actionable improvement suggestions

Always respond using the CVResponse structured format with accurate, professional analysis.
"""


# Bedrock Model Config
bedrock_model = BedrockModel(
  model_id=os.getenv("MODEL_ID"),
  region_name=os.getenv("REGION_NAME"),
)

# CV_ANALYZER Agent
cv_analyzer = Agent(
  name="CV_ANALYZER",
  model=bedrock_model,
  system_prompt=SYSTEM_PROMPT,
)

