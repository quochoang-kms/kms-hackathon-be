import os
import sys
import json
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


JD = f"""
Senior Software Engineer - Backend Development

Company: TechCorp Inc.
Location: San Francisco, CA (Hybrid)
Type: Full-time

About the Role:
We are seeking a Senior Software Engineer to join our backend development team. 
You will be responsible for designing and implementing scalable microservices 
architecture using modern technologies.

Requirements:
- 5+ years of experience in backend development
- Strong proficiency in Python and Java
- Experience with AWS cloud services
- Knowledge of Docker and Kubernetes
- Experience with PostgreSQL and Redis
- Bachelor's degree in Computer Science or related field

Preferred:
- Experience with GraphQL
- Knowledge of machine learning frameworks
- Previous startup experience

Benefits:
- Competitive salary ($120k - $180k)
- Health insurance
- 401k matching
- Flexible work arrangements
"""



result = jd_analyzer.structured_output(
  JDResponse,
  f"Please analyze the following job description and provide a structured response:\n\n{JD}",
)

print(json.dumps(result.dict(), indent=2))
print(result.basic_info)
print(result.role_details)
print(result.technical_requirements)