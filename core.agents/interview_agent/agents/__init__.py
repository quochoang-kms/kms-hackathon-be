import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    # Enhanced agents as default
    from .enhanced_coordinator import EnhancedCoordinatorAgent as CoordinatorAgent
except ImportError:
    try:
        from enhanced_coordinator import EnhancedCoordinatorAgent as CoordinatorAgent
    except ImportError:
        # Fallback coordinator
        class CoordinatorAgent:
            def __init__(self, *args, **kwargs):
                pass

try:
    from .document_processor import DocumentProcessorAgent
except ImportError:
    try:
        from document_processor import DocumentProcessorAgent
    except ImportError:
        class DocumentProcessorAgent:
            def __init__(self, *args, **kwargs):
                pass

try:
    from .question_generator import QuestionGeneratorAgent
except ImportError:
    try:
        from question_generator import QuestionGeneratorAgent
    except ImportError:
        class QuestionGeneratorAgent:
            def __init__(self, *args, **kwargs):
                pass

try:
    from .answer_tips_generator import AnswerTipsGeneratorAgent
except ImportError:
    try:
        from answer_tips_generator import AnswerTipsGeneratorAgent
    except ImportError:
        class AnswerTipsGeneratorAgent:
            def __init__(self, *args, **kwargs):
                pass

try:
    from .quality_assurance import QualityAssuranceAgent
except ImportError:
    try:
        from quality_assurance import QualityAssuranceAgent
    except ImportError:
        class QualityAssuranceAgent:
            def __init__(self, *args, **kwargs):
                pass

try:
    from .formatter import FormatterAgent
except ImportError:
    try:
        from formatter import FormatterAgent
    except ImportError:
        class FormatterAgent:
            def __init__(self, *args, **kwargs):
                pass

# Legacy support
try:
    from .coordinator import CoordinatorAgent as LegacyCoordinatorAgent
except ImportError:
    try:
        from coordinator import CoordinatorAgent as LegacyCoordinatorAgent
    except ImportError:
        LegacyCoordinatorAgent = CoordinatorAgent

try:
    from .enhanced_coordinator import EnhancedCoordinatorAgent
except ImportError:
    try:
        from enhanced_coordinator import EnhancedCoordinatorAgent
    except ImportError:
        EnhancedCoordinatorAgent = CoordinatorAgent

__all__ = [
    # Default (enhanced) exports
    "CoordinatorAgent",
    "DocumentProcessorAgent",
    "QuestionGeneratorAgent", 
    "AnswerTipsGeneratorAgent",
    "QualityAssuranceAgent",
    "FormatterAgent",
    
    # Legacy exports
    "LegacyCoordinatorAgent",
    "EnhancedCoordinatorAgent"
]
