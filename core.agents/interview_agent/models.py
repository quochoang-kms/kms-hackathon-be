from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


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


class InterviewQuestion(BaseModel):
    question: str = Field(..., description="The interview question")
    type: QuestionType = Field(..., description="Type of question")
    difficulty: str = Field(..., description="Question difficulty level")
    expected_duration: int = Field(..., description="Expected answer duration in minutes")


class SampleAnswer(BaseModel):
    question: str = Field(..., description="The original question")
    answer: str = Field(..., description="Sample answer")
    key_points: List[str] = Field(..., description="Key points covered in the answer")
    evaluation_criteria: List[str] = Field(..., description="What to look for in candidate's answer")


class InterviewRequest(BaseModel):
    jd_content: str = Field(..., description="Job description content")
    cv_content: str = Field(..., description="CV/Resume content")
    role: str = Field(..., description="Job role/position")
    level: ExperienceLevel = Field(..., description="Experience level")
    round_number: InterviewRound = Field(..., description="Interview round number")
    num_questions: int = Field(default=5, description="Number of questions to generate")


class InterviewResponse(BaseModel):
    questions: List[InterviewQuestion] = Field(..., description="Generated interview questions")
    sample_answers: List[SampleAnswer] = Field(..., description="Sample answers for the questions")
    interview_focus: str = Field(..., description="Main focus areas for this interview round")
    preparation_tips: List[str] = Field(..., description="Tips for the interviewer")


class DocumentContent(BaseModel):
    content: str = Field(..., description="Extracted document content")
    metadata: dict = Field(default_factory=dict, description="Document metadata")
    file_type: str = Field(..., description="Type of document (pdf, docx, txt)")
