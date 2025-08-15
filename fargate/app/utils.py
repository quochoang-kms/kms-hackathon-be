import asyncio
import io
import json
import re
import time
from typing import Dict, Any
from fastapi import HTTPException, UploadFile
import PyPDF2
import docx

# Semaphore for concurrent request limiting
MAX_CONCURRENT_REQUESTS = 5
request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

async def with_concurrency_limit(func, *args, **kwargs):
    """Execute function with concurrency limiting"""
    async with request_semaphore:
        return await func(*args, **kwargs)

def extract_pdf_text(content: bytes, filename: str) -> str:
    """Extract text from PDF file"""
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

def extract_docx_text(content: bytes, filename: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc_file = io.BytesIO(content)
        doc = docx.Document(doc_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to extract text from DOCX {filename}: {str(e)}"
        )

def process_file(content: bytes, file: UploadFile) -> str:
    """Process uploaded file based on type"""
    filename = file.filename.lower()
    content_type = file.content_type
    
    if content_type == 'application/pdf' or filename.endswith('.pdf'):
        return extract_pdf_text(content, file.filename)
    elif (content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or 
          filename.endswith('.docx')):
        return extract_docx_text(content, file.filename)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}. Please upload PDF or DOCX files only."
        )

def validate_inputs(jd_text: str, cv_text: str):
    """Validate input text content"""
    if len(jd_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Job description appears to be too short or invalid")
    
    if len(cv_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="CV content appears to be too short or invalid")

def parse_agent_response(response_text: str) -> Dict[str, Any]:
    """Parse JSON from agent response"""
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))
    else:
        # Fallback: try to parse the entire response as JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Failed to parse agent response")

def create_analysis_summary(jd_analysis: Dict, cv_analysis: Dict, skill_matching: Dict) -> Dict[str, Any]:
    """Create a summary of the analysis results for question generation"""
    return {
        "candidate_level": cv_analysis.get("experience_level", "Unknown"),
        "role_level": jd_analysis.get("role_level", "Unknown"),
        "matching_score": skill_matching.get("overall_matching_score", 0),
        "key_skills": skill_matching.get("matched_skills", []),
        "missing_skills": skill_matching.get("missing_critical_skills", []),
        "strong_areas": skill_matching.get("strong_areas", []),
        "red_flags": skill_matching.get("red_flags", []),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }