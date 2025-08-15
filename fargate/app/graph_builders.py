import os
from strands import Agent
from strands.multiagent import GraphBuilder
from strands.models import BedrockModel
from agents.jd_analyzer.jd_analyzer import jd_analyzer
from agents.cv_analyzer.cv_analyzer import cv_analyzer  
from agents.skill_matcher.skill_matcher import skill_matcher
from agents.question_generator.question_generator import question_generator
from conditions.conditions import is_analyzer_done, is_skill_matching_done

# Bedrock Model Config
bedrock_model = BedrockModel(
    model_id=os.getenv("MODEL_ID"),
    region_name=os.getenv("REGION_NAME"),
)

def create_skill_analysis_graph():
    """Create graph for skill matching analysis (JD + CV + Skill Matcher)"""
    
    SKILL_ORCHESTRATOR_PROMPT = """
    You are the SKILL_ORCHESTRATOR, coordinating JD analysis, CV analysis, and skill matching.
    
    Your workflow:
    1. Route to JD_ANALYZER and CV_ANALYZER in parallel
    2. Once both complete, route to SKILL_MATCHER
    3. Provide comprehensive skill matching analysis
    """
    
    orchestrator = Agent(
        name="SKILL_ORCHESTRATOR",
        model=bedrock_model,
        system_prompt=SKILL_ORCHESTRATOR_PROMPT,
    )

    builder = GraphBuilder()
    
    # Add nodes
    builder.add_node(orchestrator, "SKILL_ORCHESTRATOR")
    builder.add_node(jd_analyzer, "JD_ANALYZER")
    builder.add_node(cv_analyzer, "CV_ANALYZER")
    builder.add_node(skill_matcher, "SKILL_MATCHER")
    
    # Add edges
    builder.add_edge("SKILL_ORCHESTRATOR", "JD_ANALYZER")
    builder.add_edge("SKILL_ORCHESTRATOR", "CV_ANALYZER")
    builder.add_edge("JD_ANALYZER", "SKILL_MATCHER", condition=is_analyzer_done)
    builder.add_edge("CV_ANALYZER", "SKILL_MATCHER", condition=is_analyzer_done)
    
    builder.set_entry_point("SKILL_ORCHESTRATOR")
    
    return builder.build()

def create_question_generation_agent():
    """Create standalone question generator agent"""
    
    QUESTION_ORCHESTRATOR_PROMPT = """
    You are the QUESTION_ORCHESTRATOR, specialized in generating interview questions.
    
    You will receive:
    - Job Description Analysis
    - CV Analysis  
    - Skill Matching Results
    
    Generate tailored interview questions based on this comprehensive analysis.
    """
    
    return Agent(
        name="QUESTION_ORCHESTRATOR",
        model=bedrock_model,
        system_prompt=QUESTION_ORCHESTRATOR_PROMPT,
    )