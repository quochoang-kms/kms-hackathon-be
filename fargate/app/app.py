from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import PlainTextResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Union
import os
import sys
import asyncio
import json
import logging
from dotenv import load_dotenv
import uvicorn
import PyPDF2
import io
import re
import time
import traceback

from strands import Agent

from agents.jd_analyzer.jd_analyzer import jd_analyzer
from agents.cv_analyzer.cv_analyzer import cv_analyzer  
from agents.skill_matcher.skill_matcher import skill_matcher
from agents.question_generator.question_generator import question_generator
from models import JDResponse, CVResponse, SkillMatcherResponse, QuestionGeneratorResponse
from conditions.conditions import is_matched_skill, is_analyzer_done, is_skill_matching_done

from strands.multiagent import GraphBuilder
from strands.models import BedrockModel
from strands.types.content import ContentBlock

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the agents path to sys.path
sys.path.append('/app')

# Initialize FastAPI app
app = FastAPI(
    title="Interview Preparation API",
    description="AI-powered interview preparation system using Strands agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bedrock Model Config
bedrock_model = BedrockModel(
    model_id=os.getenv("MODEL_ID"),
    region_name=os.getenv("REGION_NAME"),
)

# Initialize the multi-agent graph
def create_interview_graph():
    """Create and configure the interview preparation agent graph"""
        
    ORCHESTRATOR_PROMPT = """
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
        system_prompt=ORCHESTRATOR_PROMPT,
    )

    # Initialize GraphBuilder
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

    return builder.build()

# Global graph instance
interview_graph = create_interview_graph() 

# Pydantic models for request/response
class InterviewRequest(BaseModel):
    job_description: str
    cv_content: str
    additional_context: Optional[str] = None

class InterviewResponse(BaseModel):
    status: str
    execution_time: Optional[float] = None
    jd_analysis: Optional[JDResponse] = None
    cv_analysis: Optional[CVResponse] = None
    skills_matching: Optional[SkillMatcherResponse] = None
    questions: Optional[QuestionGeneratorResponse] = None
    summary: Optional[dict] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for load balancer"""
    return HealthResponse(
        status="healthy",
        service="interview-preparation-api",
        version="1.0.0"
    )


# File upload endpoint for handling CV/JD uploads
@app.post("/prepare-interview")
async def prepare_interview(
    jd_file: UploadFile = File(...),
    cv_file: UploadFile = File(...),
):
    """
    Prepare interview questions using uploaded files
    """
    start_time = time.time()
    
    try:
        # Read file contents
        jd_content = await jd_file.read()
        cv_content = await cv_file.read()
        
        # Function to extract text from PDF
        def extract_pdf_text(content: bytes, filename: str) -> str:
            try:
                pdf_file = io.BytesIO(content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unable to extract text from PDF {filename}: {str(e)}"
                )
        
        # Function to safely decode text with multiple encoding attempts
        def safe_decode(content: bytes, filename: str) -> str:
            # List of common encodings to try
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    return content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try with error handling
            try:
                return content.decode('utf-8', errors='replace')
            except Exception:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unable to decode file {filename}. Please ensure it's a text file."
                )
        
        # Function to process file based on type
        def process_file(content: bytes, file: UploadFile) -> str:
            filename = file.filename.lower()
            content_type = file.content_type
            
            # Check if it's a PDF
            if content_type == 'application/pdf' or filename.endswith('.pdf'):
                return extract_pdf_text(content, file.filename)
            
            # Check if it's a text file
            elif (content_type in ['text/plain', 'application/octet-stream'] or 
                  any(filename.endswith(ext) for ext in ['.txt', '.md', '.text'])):
                return safe_decode(content, file.filename)
            
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {content_type}. Please upload PDF or text files only."
                )
        
        # Validate file types based on content type or extension
        def validate_file_type(file: UploadFile) -> None:
            allowed_types = ['text/plain', 'application/octet-stream', 'application/pdf']
            allowed_extensions = ['.txt', '.md', '.text', '.pdf']
            
            if file.content_type not in allowed_types:
                # Check file extension as fallback
                if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported file type: {file.content_type}. Please upload PDF or text files only."
                    )
        
        # Validate both files
        validate_file_type(jd_file)
        validate_file_type(cv_file)
        
        # Process files based on their type
        jd_text = process_file(jd_content, jd_file)
        cv_text = process_file(cv_content, cv_file)
        
        # Additional validation - check if decoded content makes sense
        if len(jd_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Job description appears to be too short or invalid")
        
        if len(cv_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="CV content appears to be too short or invalid")
        
        # Create content blocks for the graph
        content_blocks = [
            ContentBlock(text="Start Interview Preparation System"),
            ContentBlock(
                document={
                    "name": "JD",
                    "format": "txt",
                    "source": {
                        "bytes": jd_text.encode('utf-8'),
                    },
                }
            ),
            ContentBlock(
                document={
                    "name": "CV",
                    "format": "txt",
                    "source": {
                        "bytes": cv_text.encode('utf-8'),
                    },
                }
            ),
        ]
        
        # Execute the agent graph
        logger.info("Executing multi-agent workflow")
        result = interview_graph(content_blocks)
        
        skill_matcher_response = result.results["SKILL_MATCHER"].result.message["content"][0]["text"]
        question_generator_response = result.results["QUESTION_GENERATOR"].result.message["content"][0]["text"]

        skill_match_parser = re.search(r'```json\s*(.*?)\s*```', skill_matcher_response, re.DOTALL)
        question_generator_parser = re.search(r'```json\s*(.*?)\s*```', question_generator_response, re.DOTALL)
        if skill_match_parser:
            skill_matcher_json = json.loads(skill_match_parser.group(1))
            
        if question_generator_parser:
            question_generator_json = json.loads(question_generator_parser.group(1))
       
        response_data = {
            "status": "completed",
            "execution_time": time.time() - start_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "skill_matcher": skill_matcher_json,
            "question_generator": question_generator_json,            
        }
        
        return response_data
    
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"File processing failed after {execution_time:.2f} seconds: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Return error response instead of raising exception
        return {
            "status": "error",
            "execution_time": execution_time,
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)