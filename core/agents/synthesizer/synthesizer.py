import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from models import JDResponse
from strands import Agent
from dotenv import load_dotenv
from strands.models import BedrockModel

load_dotenv()

SYSTEM_PROMPT = """

"""

bedrock_model = BedrockModel(
  model_id=os.getenv("MODEL_ID"),
  region_name=os.getenv("REGION_NAME"),
)

jd_analyzer = Agent(
  name="SKILL_MATCHER",
  model=bedrock_model,
  system_prompt=SYSTEM_PROMPT,
)