import os
import logging
from dotenv import load_dotenv

from strands import Agent
from strands.multiagent import GraphBuilder
from strands.models import BedrockModel
from strands.types.content import ContentBlock

# Agents
from agents.jd_analyzer import jd_analyzer
from agents.cv_analyzer import cv_analyzer
from agents.skill_matcher import skill_matcher
from agents.question_generator import question_generator
from models import JDResponse, CVResponse, SkillMatcherResponse, QuestionGeneratorResponse

# Conditions
from conditions.conditions import is_matched_skill, is_analyzer_done, is_skill_matching_done

# Load environment variables
load_dotenv()


# Enable debug logs and print them to stderr
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Bedrock Model Config
bedrock_model = BedrockModel(
  model_id=os.getenv("MODEL_ID"),
  region_name=os.getenv("REGION_NAME"),
)

SYSTEM_PROMPT = """
You are the ORCHESTRATOR, a routing agent that coordinates multiple specialized AI agents in an interview preparation system.

Your role is to:
1. Analyze incoming requests and documents (JD, CV)
2. Route tasks to appropriate specialized agents:
   - JD_ANALYZER: For job description analysis
   - CV_ANALYZER: For candidate CV/resume analysis
   - SKILL_MATCHER: For matching skills between JD and CV
   - QUESTION_GENERATOR: For generating tailored interview questions
3. Coordinate the workflow between agents
4. Ensure proper data flow and task completion

When you receive documents, determine which agents need to process them and route accordingly.
Always maintain context and ensure all necessary agents are activated for comprehensive analysis.
The workflow should be: JD_ANALYZER & CV_ANALYZER → SKILL_MATCHER → QUESTION_GENERATOR
"""

orchestrator = Agent(
  name="ORCHESTRATOR",
  model=bedrock_model,
  system_prompt=SYSTEM_PROMPT,
)

# Initalize GraphBuilder
builder = GraphBuilder()

# Add Agent Nodes
builder.add_node(orchestrator, "ORCHESTRATOR")
builder.add_node(jd_analyzer, "JD_ANALYZER")
builder.add_node(cv_analyzer, "CV_ANALYZER")
builder.add_node(skill_matcher, "SKILL_MATCHER")
builder.add_node(question_generator, "QUESTION_GENERATOR")

# Add Edges
builder.add_edge("ORCHESTRATOR", "JD_ANALYZER")
builder.add_edge("ORCHESTRATOR", "CV_ANALYZER")
builder.add_edge("JD_ANALYZER", "SKILL_MATCHER", condition=is_analyzer_done)
builder.add_edge("CV_ANALYZER", "SKILL_MATCHER", condition=is_analyzer_done)
builder.add_edge("SKILL_MATCHER", "QUESTION_GENERATOR", condition=is_skill_matching_done)

# Define the entry point for the orchestrator
builder.set_entry_point("ORCHESTRATOR")


graph = builder.build()

with open("./resources/input/SAMPLE_JD.txt", "rb") as fp:
    sample_jd = fp.read()
    
with open("./resources/input/SAMPLE_CV.pdf", "rb") as fp:
    sample_cv = fp.read()

content_block = [
    ContentBlock(text="Start System Interview Prep Assistant"),    
    
    ContentBlock(
        document ={
            "name": "JD",
            "format": "txt",
            "source": {
                "bytes": sample_jd,
            },
        }
    ),
    ContentBlock(
        document ={
            "name": "CV",
            "format": "pdf",
            "source": {
                "bytes": sample_cv,
            },
        }
    ),
]

result = graph(content_block)


# Check execution status
print(f"Status: {result.status}")  # COMPLETED, FAILED, etc.

# See which nodes were executed and in what order
for node in result.execution_order:
    print(f"Executed: {node.node_id}")

# Get performance metrics
print(f"Total nodes: {result.total_nodes}")
print(f"Completed nodes: {result.completed_nodes}")
print(f"Failed nodes: {result.failed_nodes}")
print(f"Execution time: {result.execution_time}ms")
print(f"Token usage: {result.accumulated_usage}")

jd_result = result.results["JD_ANALYZER"].result
print(f"JD Analysis: {jd_result}")