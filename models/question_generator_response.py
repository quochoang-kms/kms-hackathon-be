"""Question Generator Response Pydantic Models for Strands Agent Structured Output"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class QuestionCategory(str, Enum):
    CORE_KNOWLEDGE = "core_knowledge"
    PRACTICAL_SKILLS = "practical_skills"
    TOOLS_TECHNOLOGY = "tools_technology"
    SCENARIO_PROBLEM_SOLVING = "scenario_problem_solving"
    PROCESS_BEST_PRACTICES = "process_best_practices"


class DifficultyLevel(str, Enum):
    JUNIOR = "junior"
    SENIOR = "senior"
    PRINCIPAL = "principal"


class EvaluationCriteria(BaseModel):
    clarity: str = Field(description="What to look for in terms of communication clarity")
    accuracy: str = Field(description="What technical accuracy indicators to assess")
    depth: str = Field(description="Expected depth of knowledge demonstration")
    practical_application: Optional[str] = Field(description="How well they can apply knowledge practically")


class ScoringGuide(BaseModel):
    score_1: str = Field(description="1 star - Poor performance indicators")
    score_2: str = Field(description="2 stars - Below average performance indicators") 
    score_3: str = Field(description="3 stars - Average/satisfactory performance indicators")
    score_4: str = Field(description="4 stars - Good performance indicators")
    score_5: str = Field(description="5 stars - Excellent performance indicators")


class InterviewQuestion(BaseModel):
    question_id: str = Field(description="Unique identifier for the question")
    category: QuestionCategory = Field(description="Question category classification")
    difficulty_level: DifficultyLevel = Field(description="Difficulty level of the question")
    question_text: str = Field(description="The actual interview question")
    context: Optional[str] = Field(description="Additional context or setup for the question")
    expected_answer: str = Field(description="Ideal sample answer or key points to cover")
    evaluation_rubric: EvaluationCriteria = Field(description="What to look for when evaluating")
    scoring_guide: ScoringGuide = Field(description="5-point scoring guide with descriptions")
    follow_up_questions: List[str] = Field(default=[], description="Potential follow-up questions")
    time_allocation: int = Field(description="Recommended time in minutes for this question")
    skills_assessed: List[str] = Field(description="Specific skills this question evaluates")


class CategorySummary(BaseModel):
    category: QuestionCategory = Field(description="Question category")
    question_count: int = Field(description="Number of questions in this category")
    total_time: int = Field(description="Total time allocated for this category in minutes")
    focus_areas: List[str] = Field(description="Key focus areas for this category")
    rationale: str = Field(description="Why these questions were chosen for this category")


class QuestionGeneratorResponse(BaseModel):
    """Question Generator Analysis Response following Strands Agent structured output"""
    
    # Question sets
    questions: List[InterviewQuestion] = Field(description="Generated interview questions (15 total)")
    category_summaries: List[CategorySummary] = Field(description="Summary for each category")
    
    # Interview metadata
    target_position: str = Field(description="Target job position")
    candidate_level: str = Field(description="Assessed candidate level")
    total_interview_time: int = Field(description="Total recommended interview time in minutes")
    interview_focus: List[str] = Field(description="Key areas of focus for this interview")
    
    # Customization based on analysis
    strengths_to_validate: List[str] = Field(description="Candidate strengths to validate through questions")
    gaps_to_assess: List[str] = Field(description="Skill gaps to assess during interview")
    red_flags_to_investigate: List[str] = Field(description="Concerns to investigate further")
    
    # Question distribution
    core_knowledge_count: int = Field(description="Number of core knowledge questions")
    practical_skills_count: int = Field(description="Number of practical skills questions") 
    tools_technology_count: int = Field(description="Number of tools & technology questions")
    scenario_problem_solving_count: int = Field(description="Number of scenario-based questions")
    process_best_practices_count: int = Field(description="Number of process & best practices questions")
    
    # Interviewer guidance
    interview_strategy: str = Field(description="Recommended interview strategy and approach")
    key_decision_points: List[str] = Field(description="Critical areas that will influence hiring decision")
    preparation_notes: List[str] = Field(description="Notes for interviewer preparation")
    
    # Strands Agent metadata
    status: str = "completed"
    timestamp: Optional[str] = None
    processing_time: Optional[float] = None
    agent_version: str = "1.0.0"
    
    class Config:
        use_enum_values = True
