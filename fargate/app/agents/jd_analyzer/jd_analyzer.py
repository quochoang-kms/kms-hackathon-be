import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from models import JDResponse
from strands import Agent
from dotenv import load_dotenv
from strands.models import BedrockModel

load_dotenv()

SYSTEM_PROMPT = """
You are JD_ANALYZER, a specialized AI agent that analyzes job descriptions and returns structured JSON output using the JDResponse format.

When you receive a job description, analyze it and respond with structured data including:
- Basic information (job title, company, location, etc.)
- Role details and responsibilities  
- Technical requirements
- Qualifications (must-have and nice-to-have)
- Skills analysis
- Company culture information
- Analysis insights

Always respond using the JDResponse structured format.
"""

bedrock_model = BedrockModel(
  model_id=os.getenv("MODEL_ID"),
  region_name=os.getenv("REGION_NAME"),
)

jd_analyzer = Agent(
  name="JD_ANALYZER",
  model=bedrock_model,
  system_prompt=SYSTEM_PROMPT,
)

