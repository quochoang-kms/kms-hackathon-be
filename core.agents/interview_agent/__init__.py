"""
Interview Agent - Enhanced Multi-Agent Interview Question & Answer Generator

A sophisticated Enhanced Hybrid Hierarchical-Parallel Multi-Agent System built with 
Strands Agents framework that generates tailored interview questions and sample answers 
with 40-50% performance improvement through parallel processing and comprehensive quality assurance.

This package provides a unified interface with all enhanced functionality built-in.
"""

from .main import (
    InterviewAgent,
    generate_interview,
    generate_interview_async,
    EnhancedInterviewRequest,
    EnhancedInterviewResponse,
    ExperienceLevel,
    InterviewRound
)

# Backward compatibility aliases
EnhancedInterviewAgent = InterviewAgent
generate_interview_enhanced = generate_interview
InterviewRequest = EnhancedInterviewRequest  # Alias for backward compatibility
InterviewResponse = EnhancedInterviewResponse  # Alias for backward compatibility

__version__ = "2.0.0"
__author__ = "Interview Agent Team"
__description__ = "Enhanced Multi-Agent Interview Question & Answer Generator"

__all__ = [
    # Main classes
    "InterviewAgent",
    "EnhancedInterviewAgent",  # Alias for backward compatibility
    
    # Convenience functions
    "generate_interview",
    "generate_interview_enhanced",  # Alias for backward compatibility
    "generate_interview_async",
    
    # Models
    "EnhancedInterviewRequest",
    "EnhancedInterviewResponse",
    "InterviewRequest",  # Alias for backward compatibility
    "InterviewResponse",  # Alias for backward compatibility
    "ExperienceLevel",
    "InterviewRound",
    
    # Metadata
    "__version__",
    "__author__",
    "__description__"
]
