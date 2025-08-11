from strands import Agent
from strands.models import BedrockModel

# Fix imports for standalone execution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.document_parser import parse_pdf, parse_docx, parse_text_file
from tools.content_analyzer import analyze_jd_content, analyze_cv_content


class DocumentProcessorAgent:
    """Agent responsible for processing and analyzing documents (JD and CV)."""
    
    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2"):
        """
        Initialize the Document Processor Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.3,
        )
        
        self.agent = Agent(
            model=self.model,
            tools=[parse_pdf, parse_docx, parse_text_file, analyze_jd_content, analyze_cv_content],
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the document processor agent."""
        return """
        You are a Document Processing Agent specialized in analyzing job descriptions and CVs/resumes.
        
        Your responsibilities:
        1. Extract and parse content from PDF, DOCX, and text files
        2. Analyze job descriptions to identify key requirements, skills, and responsibilities
        3. Analyze CVs to extract candidate information, skills, experience, and qualifications
        4. Provide structured analysis that can be used by other agents for interview preparation
        
        When processing documents:
        - Extract all relevant information accurately
        - Identify technical and soft skills
        - Note experience levels and requirements
        - Highlight key qualifications and achievements
        - Maintain professional and objective analysis
        
        Always provide comprehensive analysis in a structured format that other agents can easily consume.
        """
    
    def process_documents(self, jd_file_path: str, cv_file_path: str) -> dict:
        """
        Process job description and CV documents.
        
        Args:
            jd_file_path: Path to job description file
            cv_file_path: Path to CV file
            
        Returns:
            dict: Processed document analysis
        """
        prompt = f"""
        Please process and analyze the following documents:
        
        1. Job Description file: {jd_file_path}
        2. CV/Resume file: {cv_file_path}
        
        For each document:
        1. First, parse the document to extract the text content
        2. Then analyze the content to extract key information
        
        Provide a comprehensive analysis including:
        - Extracted content from both documents
        - Key skills and requirements from the JD
        - Candidate skills and experience from the CV
        - Alignment between JD requirements and CV qualifications
        - Areas where the candidate excels
        - Potential gaps or areas for questioning
        
        Format your response as a structured analysis that can be used for interview preparation.
        """
        
        response = self.agent(prompt)
        return {"analysis": response.message, "status": "completed"}
    
    def process_content_directly(self, jd_content: str, cv_content: str) -> dict:
        """
        Process job description and CV content directly (when content is already extracted).
        
        Args:
            jd_content: Job description text content
            cv_content: CV text content
            
        Returns:
            dict: Processed document analysis
        """
        prompt = f"""
        Please analyze the following job description and CV content:
        
        JOB DESCRIPTION:
        {jd_content}
        
        CV/RESUME:
        {cv_content}
        
        Provide a comprehensive analysis including:
        1. Key requirements and skills from the job description
        2. Candidate's skills, experience, and qualifications from the CV
        3. Alignment between job requirements and candidate qualifications
        4. Candidate's strengths that match the role
        5. Potential areas for deeper questioning during the interview
        6. Technical skills assessment
        7. Experience level evaluation
        
        Structure your analysis in a clear, organized format that will help generate relevant interview questions.
        """
        
        response = self.agent(prompt)
        return {"analysis": response.message, "status": "completed"}
