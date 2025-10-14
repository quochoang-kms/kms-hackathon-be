import os
import sys

from strands.models.openai import OpenAIModel

from tools.check_valid_company import check_valid_company
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

openai_model = OpenAIModel(
    client_args={"api_key": os.getenv("OPENAI_API_KEY")},
    model_id="gpt-4o-mini",
)

# CV_ANALYZER Agent
cv_analyzer = Agent(
  name="CV_ANALYZER",
  model=openai_model,
  system_prompt=SYSTEM_PROMPT,
  tools=[check_valid_company],
)
