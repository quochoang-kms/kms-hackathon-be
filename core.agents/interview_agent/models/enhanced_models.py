from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

# Import from the parent models module
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import ExperienceLevel, InterviewRound, QuestionType
except ImportError:
    # Fallback definitions if parent models not available
    class ExperienceLevel(str, Enum):
        JUNIOR = "Junior"
        MID = "Mid"
        SENIOR = "Senior"
        LEAD = "Lead"
        PRINCIPAL = "Principal"

    class InterviewRound(int, Enum):
        SCREENING = 1
        TECHNICAL = 2
        BEHAVIORAL = 3
        FINAL = 4

    class QuestionType(str, Enum):
        TECHNICAL = "technical"
        BEHAVIORAL = "behavioral"
        SITUATIONAL = "situational"
        CULTURAL_FIT = "cultural_fit"


class QualityMetrics(BaseModel):
    """Quality metrics for generated content."""
    relevance_score: float = Field(..., description="Relevance to role and requirements (0-1)")
    clarity_score: float = Field(..., description="Clarity and understandability (0-1)")
    completeness_score: float = Field(..., description="Completeness of content (0-1)")
    consistency_score: float = Field(..., description="Consistency with other content (0-1)")
    overall_score: float = Field(..., description="Overall quality score (0-1)")


class EnhancedInterviewQuestion(BaseModel):
    """Enhanced interview question with quality metrics."""
    question: str = Field(..., description="The interview question")
    type: QuestionType = Field(..., description="Type of question")
    difficulty: str = Field(..., description="Question difficulty level")
    expected_duration: int = Field(..., description="Expected answer duration in minutes")
    quality_metrics: QualityMetrics = Field(..., description="Quality assessment metrics")
    tags: List[str] = Field(default_factory=list, description="Question tags for categorization")
    follow_up_questions: List[str] = Field(default_factory=list, description="Suggested follow-up questions")


class EnhancedSampleAnswer(BaseModel):
    """Enhanced sample answer with quality metrics."""
    question: str = Field(..., description="The original question")
    answer: str = Field(..., description="Sample answer")
    key_points: List[str] = Field(..., description="Key points covered in the answer")
    evaluation_criteria: List[str] = Field(..., description="What to look for in candidate's answer")
    quality_metrics: QualityMetrics = Field(..., description="Quality assessment metrics")
    answer_framework: str = Field(..., description="Framework used (STAR, technical, etc.)")
    red_flags: List[str] = Field(default_factory=list, description="Warning signs in candidate responses")
    excellent_indicators: List[str] = Field(default_factory=list, description="Signs of exceptional responses")


class ProcessingPhase(str, Enum):
    """Processing phases in the enhanced workflow."""
    DOCUMENT_ANALYSIS = "document_analysis"
    PARALLEL_GENERATION = "parallel_generation"
    QUALITY_ASSURANCE = "quality_assurance"
    FINAL_FORMATTING = "final_formatting"


class AgentPerformanceMetrics(BaseModel):
    """Performance metrics for individual agents."""
    agent_name: str = Field(..., description="Name of the agent")
    processing_time: float = Field(..., description="Processing time in seconds")
    token_usage: int = Field(..., description="Number of tokens used")
    success_rate: float = Field(..., description="Success rate (0-1)")
    error_count: int = Field(default=0, description="Number of errors encountered")


class EnhancedInterviewRequest(BaseModel):
    """Enhanced interview generation request."""
    jd_content: str = Field(..., description="Job description content")
    cv_content: str = Field(..., description="CV/Resume content")
    role: str = Field(..., description="Job role/position")
    level: ExperienceLevel = Field(..., description="Experience level")
    round_number: InterviewRound = Field(..., description="Interview round number")
    num_questions: int = Field(default=5, description="Number of questions to generate")
    
    # Enhanced options
    enable_parallel_processing: bool = Field(default=True, description="Enable parallel processing")
    quality_assurance: bool = Field(default=True, description="Enable quality assurance")
    include_follow_ups: bool = Field(default=True, description="Include follow-up questions")
    custom_focus_areas: List[str] = Field(default_factory=list, description="Custom focus areas")
    difficulty_preference: Optional[str] = Field(None, description="Preferred difficulty level")


class EnhancedInterviewResponse(BaseModel):
    """Enhanced interview response with quality metrics."""
    questions: List[EnhancedInterviewQuestion] = Field(..., description="Generated interview questions")
    sample_answers: List[EnhancedSampleAnswer] = Field(..., description="Sample answers for the questions")
    interview_focus: str = Field(..., description="Main focus areas for this interview round")
    preparation_tips: List[str] = Field(..., description="Tips for the interviewer")
    
    # Enhanced response data
    overall_quality_score: float = Field(..., description="Overall quality score (0-1)")
    processing_metrics: List[AgentPerformanceMetrics] = Field(..., description="Performance metrics per agent")
    quality_report: Dict[str, Any] = Field(..., description="Detailed quality assessment report")
    generation_metadata: Dict[str, Any] = Field(..., description="Generation process metadata")
    
    # Interviewer guidance
    interview_structure: Dict[str, Any] = Field(..., description="Suggested interview structure")
    evaluation_framework: Dict[str, Any] = Field(..., description="Comprehensive evaluation framework")
    candidate_assessment_guide: List[str] = Field(..., description="Guide for assessing candidate responses")


class QualityAssessmentReport(BaseModel):
    """Comprehensive quality assessment report."""
    overall_assessment: str = Field(..., description="Overall quality assessment summary")
    question_quality: Dict[str, float] = Field(..., description="Quality scores per question")
    answer_quality: Dict[str, float] = Field(..., description="Quality scores per answer")
    consistency_analysis: Dict[str, Any] = Field(..., description="Consistency analysis results")
    improvement_suggestions: List[str] = Field(..., description="Suggestions for improvement")
    validation_results: Dict[str, bool] = Field(..., description="Validation check results")


class ParallelProcessingResult(BaseModel):
    """Result from parallel processing phase."""
    questions_result: Dict[str, Any] = Field(..., description="Question generation results")
    answers_result: Dict[str, Any] = Field(..., description="Answer generation results")
    quality_result: Dict[str, Any] = Field(..., description="Quality assessment results")
    processing_time: float = Field(..., description="Total parallel processing time")
    success_status: Dict[str, bool] = Field(..., description="Success status per task")


class InterviewerGuidance(BaseModel):
    """Comprehensive interviewer guidance."""
    pre_interview_preparation: List[str] = Field(..., description="Pre-interview preparation steps")
    interview_flow: Dict[str, Any] = Field(..., description="Suggested interview flow")
    question_timing: Dict[str, int] = Field(..., description="Recommended timing per question")
    evaluation_rubric: Dict[str, Any] = Field(..., description="Detailed evaluation rubric")
    common_pitfalls: List[str] = Field(..., description="Common interviewing pitfalls to avoid")
    best_practices: List[str] = Field(..., description="Interview best practices")


class CandidateProfile(BaseModel):
    """Enhanced candidate profile from CV analysis."""
    skills_match: Dict[str, float] = Field(..., description="Skills match percentage per skill")
    experience_alignment: float = Field(..., description="Experience alignment score (0-1)")
    strengths: List[str] = Field(..., description="Identified candidate strengths")
    potential_gaps: List[str] = Field(..., description="Potential skill or experience gaps")
    interview_focus_areas: List[str] = Field(..., description="Recommended focus areas for interview")
    risk_assessment: Dict[str, str] = Field(..., description="Risk assessment for different areas")


class JobRequirementAnalysis(BaseModel):
    """Enhanced job requirement analysis."""
    critical_skills: List[str] = Field(..., description="Critical skills for the role")
    nice_to_have_skills: List[str] = Field(..., description="Nice-to-have skills")
    experience_requirements: Dict[str, Any] = Field(..., description="Experience requirements breakdown")
    role_complexity: str = Field(..., description="Role complexity assessment")
    interview_priorities: List[str] = Field(..., description="Interview priority areas")
    success_criteria: List[str] = Field(..., description="Success criteria for the role")
