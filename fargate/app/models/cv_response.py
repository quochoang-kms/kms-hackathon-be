"""CV Response Pydantic Models for Strands Agent Structured Output"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ExperienceLevel(str, Enum):
    JUNIOR = "junior"
    SENIOR = "senior"
    PRINCIPAL = "principal"


class CandidateProfile(BaseModel):
    full_name: str = Field(description="Full name of the candidate")
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class ProfessionalSummary(BaseModel):
    title: str = Field(description="Current or desired job title")
    years_experience: int = Field(description="Total years of professional experience")
    summary: str = Field(description="Professional summary or objective")
    key_achievements: List[str] = Field(description="Notable achievements")


class WorkExperience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: List[str]
    achievements: List[str]
    technologies: List[str]


class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: Optional[int] = None
    gpa: Optional[str] = None
    relevant_coursework: List[str] = []


class Certification(BaseModel):
    name: str = Field(description="Certification name")
    issuer: str = Field(description="Issuing organization")
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None


class TechnicalSkills(BaseModel):
    programming_languages: List[str]
    frameworks_tools: List[str]
    platforms: List[str]
    databases: List[str]
    certifications: List[Certification]
    skill_levels: Dict[str, str] = Field(description="Skill name to proficiency level mapping")


class CVSkillsAnalysis(BaseModel):
    hard_skills: List[str]
    soft_skills: List[str]
    domain_expertise: List[str]
    skill_gaps: List[str] = Field(description="Identified skill gaps")


class CVAnalysis(BaseModel):
    experience_level: ExperienceLevel
    completeness_score: int = Field(ge=1, le=10)
    strengths: List[str]
    weaknesses: List[str]
    red_flags: List[str]
    missing_sections: List[str]
    recommendations: List[str]


class CVResponse(BaseModel):
    """CV Analysis Response following Strands Agent structured output"""
    
    candidate_profile: CandidateProfile = Field(description="Basic candidate information")
    professional_summary: ProfessionalSummary = Field(description="Professional summary and experience")
    work_experience: List[WorkExperience] = Field(description="Work experience history")
    education: List[Education] = Field(description="Educational background")
    technical_skills: TechnicalSkills = Field(description="Technical skills and certifications")
    skills_analysis: CVSkillsAnalysis = Field(description="Analysis of candidate skills")
    analysis: CVAnalysis = Field(description="Overall CV analysis and recommendations")
    
    # Strands Agent metadata
    status: str = "completed"
    timestamp: Optional[str] = None
    processing_time: Optional[float] = None
    agent_version: str = "1.0.0"
    
    class Config:
        use_enum_values = True
