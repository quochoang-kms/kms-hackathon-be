# Import enhanced models as default
from .enhanced_models import (
    EnhancedInterviewRequest as InterviewRequest, 
    EnhancedInterviewResponse as InterviewResponse,
    QualityMetrics, 
    AgentPerformanceMetrics, 
    EnhancedInterviewQuestion as InterviewQuestion, 
    EnhancedSampleAnswer as SampleAnswer,
    ExperienceLevel,
    InterviewRound,
    QuestionType
)

# Legacy imports
from .enhanced_models import (
    EnhancedInterviewRequest, 
    EnhancedInterviewResponse,
    EnhancedInterviewQuestion, 
    EnhancedSampleAnswer
)

__all__ = [
    # Default (enhanced) exports
    "InterviewRequest", 
    "InterviewResponse",
    "InterviewQuestion", 
    "SampleAnswer",
    "QualityMetrics", 
    "AgentPerformanceMetrics",
    "ExperienceLevel", 
    "InterviewRound", 
    "QuestionType",
    
    # Legacy exports
    "EnhancedInterviewRequest", 
    "EnhancedInterviewResponse",
    "EnhancedInterviewQuestion", 
    "EnhancedSampleAnswer"
]
