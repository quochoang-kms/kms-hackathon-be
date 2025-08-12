"""Interview Preparation Agents Package"""

from .document_parser import DocumentParserAgent
from .jd_analyzer import JDAnalyzerAgent
from .cv_analyzer import CVAnalyzerAgent
from .skills_matcher import SkillsMatcherAgent
from .question_generator import QuestionGeneratorAgent
from .answer_evaluator import AnswerEvaluatorAgent
from .interview_system import InterviewPreparationSystem

# Experience level constants
EXPERIENCE_LEVELS = ["Junior", "Mid", "Senior", "Lead", "Principal"]

# Interview round constants
INTERVIEW_ROUNDS = {
    1: "Screening",
    2: "Technical", 
    3: "Behavioral",
    4: "Final"
}

# Question types
QUESTION_TYPES = ["Technical", "Behavioral", "Situational", "Cultural Fit"]

# Interview personas
INTERVIEW_PERSONAS = ["Friendly", "Serious", "Analytical", "Collaborative", "Challenging"]

__all__ = [
    "DocumentParserAgent",
    "JDAnalyzerAgent", 
    "CVAnalyzerAgent",
    "SkillsMatcherAgent",
    "QuestionGeneratorAgent",
    "AnswerEvaluatorAgent",
    "InterviewPreparationSystem",
    "EXPERIENCE_LEVELS",
    "INTERVIEW_ROUNDS",
    "QUESTION_TYPES",
    "INTERVIEW_PERSONAS"
]