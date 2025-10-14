import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from strands import Agent
from dotenv import load_dotenv
from strands.models import BedrockModel

# Load environment variables
load_dotenv()

# Load system prompt from file
system_prompt_path = os.path.join(os.path.dirname(__file__), 'SYSTEM_PROMPT.md')
with open(system_prompt_path, 'r') as f:
  SYSTEM_PROMPT = f.read()

# Bedrock Model Config
bedrock_model = BedrockModel(
  model_id=os.getenv("MODEL_ID"),
  region_name=os.getenv("REGION_NAME"),
)

# SKILL_MATCHER Agent
skill_matcher = Agent(
  name="SKILL_MATCHER",
  model=bedrock_model,
  system_prompt=SYSTEM_PROMPT,
)