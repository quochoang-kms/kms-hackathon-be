"""JD Response Pydantic Models for Strands Agent Structured Output"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ComplexityLevel(str, Enum):
    JUNIOR = "junior"
    SENIOR = "senior"
    PRINCIPAL = "principal"


class MarketCompetitiveness(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class BasicInfo(BaseModel):
    job_title: str = Field(description="Title of the job position")
    company: str = Field(description="Name of the company offering the job")
    location: str = Field(description="Location of the job")
    job_type: str 
    employment_type: str
    experience_level: str
    salary_range: Optional[str] = None


class RoleDetails(BaseModel):
    department: str
    summary: str
    key_responsibilities: List[str]
    success_metrics: List[str]


class TechnicalRequirements(BaseModel):
    programming_languages: List[str]
    frameworks_tools: List[str]
    platforms: List[str]
    certifications: List[str]
    experience_years: Dict[str, int]


class Qualifications(BaseModel):
    must_have: List[str]
    nice_to_have: List[str]
    education: str
    certifications: List[str]


class SkillPriority(BaseModel):
    critical: List[str]
    important: List[str]
    beneficial: List[str]


class SkillsAnalysis(BaseModel):
    hard_skills: List[str]
    soft_skills: List[str]
    domain_expertise: List[str]
    skill_priority: SkillPriority


class CompanyCulture(BaseModel):
    company_size: str
    values: List[str]
    benefits: List[str]
    work_environment: str


class Analysis(BaseModel):
    complexity_level: ComplexityLevel
    market_competitiveness: MarketCompetitiveness
    completeness_score: int = Field(ge=1, le=10)
    red_flags: List[str]
    missing_info: List[str]
    key_insights: List[str]


class JDResponse(BaseModel):
    """JD Analysis Response following Strands Agent structured output"""
    
    basic_info: BasicInfo = Field(description="Basic information about the job")
    role_details: RoleDetails = Field(description="Details about the job role")
    technical_requirements: TechnicalRequirements = Field(description="Technical requirements for the job")
    qualifications: Qualifications = Field(description="Qualifications required for the job")
    skills_analysis: SkillsAnalysis = Field(description="Analysis of required skills")
    company_culture: CompanyCulture = Field(description="Company culture and environment")
    analysis: Analysis = Field(description="Overall analysis of the job description")
    
    # Strands Agent metadata
    status: str = "completed"
    timestamp: Optional[str] = None
    processing_time: Optional[float] = None
    agent_version: str = "1.0.0"
    
    class Config:
        use_enum_values = True