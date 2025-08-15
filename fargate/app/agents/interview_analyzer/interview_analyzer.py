import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from strands import Agent
from dotenv import load_dotenv
from strands.models import BedrockModel

load_dotenv()

SYSTEM_PROMPT = """
You are a Interview Analyzer, a specialized AI agent that analyzes interview preparation  (skill match, missing skill, red flag, questions/expected answer, criteira, ... guiding score) and returns structured JSON output using the JDResponse format.

When you receive a interview prep, analyze it and respond with structured data including:
- Basic information (job title, company, location, etc.)
- Questions/Answers (questions asked, answers given)
- Key insights (skills, qualifications, etc.)
- Any other relevant information from the transcript.

Always respond using the JDResponse structured format.
"""

bedrock_model = BedrockModel(
  model_id=os.getenv("MODEL_ID"),
  region_name=os.getenv("REGION_NAME"),
)

interview_analyzer = Agent(
  name="INTERVIEW_ANALYZER",
  model=bedrock_model,
  system_prompt=SYSTEM_PROMPT,
)
