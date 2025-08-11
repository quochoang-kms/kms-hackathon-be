# Import enhanced models as default
from .enhanced_models import (
    EnhancedInterviewRequest as InterviewRequest, 
    EnhancedInterviewResponse as InterviewResponse,
    QualityMetrics, 
    AgentPerformanceMetrics, 
    EnhancedInterviewQuestion as InterviewQuestion, 
    EnhancedAnswerTips as AnswerTips,
    ExperienceLevel,
    InterviewRound,
    QuestionType
)

# Legacy imports and backward compatibility
from .enhanced_models import (
    EnhancedInterviewRequest, 
    EnhancedInterviewResponse,
    EnhancedInterviewQuestion, 
    EnhancedAnswerTips
)

# Backward compatibility aliases
SampleAnswer = EnhancedAnswerTips  # For backward compatibility
EnhancedSampleAnswer = EnhancedAnswerTips  # For backward compatibility

__all__ = [
    # Default (enhanced) exports
    "InterviewRequest", 
    "InterviewResponse",
    "InterviewQuestion", 
    "AnswerTips",
    "QualityMetrics", 
    "AgentPerformanceMetrics",
    "ExperienceLevel", 
    "InterviewRound", 
    "QuestionType",
    
    # Legacy exports and backward compatibility
    "EnhancedInterviewRequest", 
    "EnhancedInterviewResponse",
    "EnhancedInterviewQuestion", 
    "EnhancedAnswerTips",
    "SampleAnswer",  # Backward compatibility alias
    "EnhancedSampleAnswer"  # Backward compatibility alias
]
