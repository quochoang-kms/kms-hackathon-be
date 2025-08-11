import os
from typing import Union
from .models import InterviewRequest, InterviewResponse, ExperienceLevel, InterviewRound
from .agents.coordinator import CoordinatorAgent
from .tools.document_parser import parse_pdf, parse_docx, parse_text_file


class InterviewAgent:
    """
    Main Interview Agent class that provides a simple interface for generating
    interview questions and sample answers using a multi-agent architecture.
    """
    
    def __init__(self, 
                 model_id: str = "apac.anthropic.claude-sonnet-4-20250514-v1:0",
                 region: str = "ap-southeast-1"):
        """
        Initialize the Interview Agent.
        
        Args:
            model_id: Bedrock model ID to use for all agents
            region: AWS region for Bedrock API calls
        """
        self.coordinator = CoordinatorAgent(model_id, region)
        self.model_id = model_id
        self.region = region
    
    def generate_interview_content(self,
                                 jd_content: str = None,
                                 cv_content: str = None,
                                 jd_file: str = None,
                                 cv_file: str = None,
                                 role: str = None,
                                 level: Union[str, ExperienceLevel] = None,
                                 round_number: Union[int, InterviewRound] = None,
                                 num_questions: int = 5) -> InterviewResponse:
        """
        Generate interview questions and sample answers.
        
        Args:
            jd_content: Job description text content (optional if jd_file provided)
            cv_content: CV text content (optional if cv_file provided)
            jd_file: Path to job description file (PDF, DOCX, or TXT)
            cv_file: Path to CV file (PDF, DOCX, or TXT)
            role: Job role/position title
            level: Experience level (Junior, Mid, Senior, Lead, Principal)
            round_number: Interview round (1-4)
            num_questions: Number of questions to generate (default: 5)
            
        Returns:
            InterviewResponse: Generated questions and answers with metadata
            
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        # Validate inputs
        if not role:
            raise ValueError("Role is required")
        
        if not level:
            raise ValueError("Experience level is required")
        
        if not round_number:
            raise ValueError("Round number is required")
        
        # Convert string inputs to enums if needed
        if isinstance(level, str):
            try:
                level = ExperienceLevel(level)
            except ValueError:
                raise ValueError(f"Invalid experience level: {level}. Must be one of: {[e.value for e in ExperienceLevel]}")
        
        if isinstance(round_number, int):
            try:
                round_number = InterviewRound(round_number)
            except ValueError:
                raise ValueError(f"Invalid round number: {round_number}. Must be 1-4")
        
        # Get content from files if not provided directly
        if not jd_content and jd_file:
            jd_content = self._extract_file_content(jd_file)
        
        if not cv_content and cv_file:
            cv_content = self._extract_file_content(cv_file)
        
        if not jd_content:
            raise ValueError("Job description content or file is required")
        
        if not cv_content:
            raise ValueError("CV content or file is required")
        
        # Create request object
        request = InterviewRequest(
            jd_content=jd_content,
            cv_content=cv_content,
            role=role,
            level=level,
            round_number=round_number,
            num_questions=num_questions
        )
        
        # Generate interview content using coordinator
        return self.coordinator.generate_interview_content(request)
    
    def generate_from_files(self,
                           jd_file_path: str,
                           cv_file_path: str,
                           role: str,
                           level: Union[str, ExperienceLevel],
                           round_number: Union[int, InterviewRound],
                           num_questions: int = 5) -> InterviewResponse:
        """
        Generate interview content directly from file paths.
        
        Args:
            jd_file_path: Path to job description file
            cv_file_path: Path to CV file
            role: Job role
            level: Experience level
            round_number: Interview round
            num_questions: Number of questions to generate
            
        Returns:
            InterviewResponse: Generated interview content
        """
        # Convert string inputs to enums if needed
        if isinstance(level, str):
            level = ExperienceLevel(level)
        
        if isinstance(round_number, int):
            round_number = InterviewRound(round_number)
        
        return self.coordinator.generate_from_files(
            jd_file_path,
            cv_file_path,
            role,
            level,
            round_number,
            num_questions
        )
    
    def _extract_file_content(self, file_path: str) -> str:
        """
        Extract content from a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Extracted text content
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                result = parse_pdf(file_path)
                return result.content
            elif file_ext in ['.docx', '.doc']:
                result = parse_docx(file_path)
                return result.content
            elif file_ext in ['.txt', '.md']:
                result = parse_text_file(file_path)
                return result.content
            else:
                raise ValueError(f"Unsupported file type: {file_ext}. Supported types: .pdf, .docx, .doc, .txt, .md")
        except Exception as e:
            raise Exception(f"Error extracting content from {file_path}: {str(e)}")
    
    def get_supported_levels(self) -> list:
        """Get list of supported experience levels."""
        return [level.value for level in ExperienceLevel]
    
    def get_supported_rounds(self) -> list:
        """Get list of supported interview rounds."""
        return [round_num.value for round_num in InterviewRound]
    
    def validate_inputs(self,
                       role: str = None,
                       level: str = None,
                       round_number: int = None) -> dict:
        """
        Validate input parameters and return validation results.
        
        Args:
            role: Job role to validate
            level: Experience level to validate
            round_number: Round number to validate
            
        Returns:
            dict: Validation results with errors and warnings
        """
        errors = []
        warnings = []
        
        if role:
            if len(role.strip()) < 3:
                errors.append("Role must be at least 3 characters long")
        
        if level:
            try:
                ExperienceLevel(level)
            except ValueError:
                errors.append(f"Invalid experience level: {level}. Valid options: {self.get_supported_levels()}")
        
        if round_number:
            try:
                InterviewRound(round_number)
            except ValueError:
                errors.append(f"Invalid round number: {round_number}. Valid options: {self.get_supported_rounds()}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


# Convenience function for quick usage
def generate_interview(jd_content: str = None,
                      cv_content: str = None,
                      jd_file: str = None,
                      cv_file: str = None,
                      role: str = None,
                      level: str = None,
                      round_number: int = None,
                      num_questions: int = 5,
                      model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                      region: str = "us-west-2") -> InterviewResponse:
    """
    Convenience function to generate interview content with minimal setup.
    
    Args:
        jd_content: Job description text
        cv_content: CV text
        jd_file: Path to JD file
        cv_file: Path to CV file
        role: Job role
        level: Experience level
        round_number: Interview round (1-4)
        num_questions: Number of questions
        model_id: Bedrock model ID
        region: AWS region
        
    Returns:
        InterviewResponse: Generated interview content
    """
    agent = InterviewAgent(model_id, region)
    return agent.generate_interview_content(
        jd_content=jd_content,
        cv_content=cv_content,
        jd_file=jd_file,
        cv_file=cv_file,
        role=role,
        level=level,
        round_number=round_number,
        num_questions=num_questions
    )
