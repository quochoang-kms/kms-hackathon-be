"""Skill Matcher Response Pydantic Models for Strands Agent Structured Output"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class MatchLevel(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class ImpactLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReadinessLevel(str, Enum):
    READY = "ready"
    NEARLY_READY = "nearly_ready"
    NEEDS_DEVELOPMENT = "needs_development"
    NOT_READY = "not_ready"


class MatchedSkill(BaseModel):
    skill_name: str = Field(description="Name of the matched skill")
    confidence_score: int = Field(ge=0, le=100, description="Confidence score for the match (0-100)")
    jd_requirement_level: str = Field(description="Required proficiency level from JD")
    cv_proficiency_level: str = Field(description="Candidate's proficiency level from CV")
    match_quality: MatchLevel = Field(description="Quality of the match")
    evidence: List[str] = Field(description="Evidence from CV supporting this skill")


class MissingSkill(BaseModel):
    skill_name: str = Field(description="Name of the missing skill")
    impact_level: ImpactLevel = Field(description="Impact of missing this skill")
    priority: str = Field(description="Priority level (critical/important/beneficial)")
    suggested_learning_path: Optional[str] = None
    can_be_learned_quickly: bool = False
    alternative_skills: List[str] = Field(default=[], description="Alternative skills that could compensate")


class LevelGapAnalysis(BaseModel):
    target_level: str = Field(description="Target position level (junior/senior/principal)")
    candidate_current_level: str = Field(description="Candidate's assessed current level")
    level_gap: str = Field(description="Gap between current and target level")
    key_competencies_missing: List[str] = Field(description="Key competencies missing for the level")
    development_areas: List[str] = Field(description="Areas needing development for the level")
    estimated_time_to_readiness: Optional[str] = None


class StrongArea(BaseModel):
    area_name: str = Field(description="Name of the strong area")
    description: str = Field(description="Description of why this is a strength")
    exceeds_requirement_by: str = Field(description="How much it exceeds requirements")
    competitive_advantage: bool = Field(description="Whether this gives competitive advantage")


class RedFlag(BaseModel):
    concern: str = Field(description="Description of the red flag or concern")
    severity: str = Field(description="Severity level (high/medium/low)")
    potential_impact: str = Field(description="Potential impact on job performance")
    mitigation_strategy: Optional[str] = None


class ReadinessAssessment(BaseModel):
    overall_readiness: ReadinessLevel = Field(description="Overall readiness for the position")
    readiness_score: int = Field(ge=0, le=100, description="Readiness score (0-100)")
    key_blockers: List[str] = Field(description="Key blockers preventing readiness")
    quick_wins: List[str] = Field(description="Quick improvements that can boost readiness")
    long_term_development: List[str] = Field(description="Long-term development areas")
    recommended_timeline: Optional[str] = None


class SkillMatcherResponse(BaseModel):
    """Skill Matcher Analysis Response following Strands Agent structured output"""
    
    overall_match_score: int = Field(ge=0, le=100, description="Overall matching score (0-100)")
    matched_skills: List[MatchedSkill] = Field(description="Skills that match between CV and JD")
    missing_critical_skills: List[MissingSkill] = Field(description="Critical skills missing from CV")
    level_gap_analysis: LevelGapAnalysis = Field(description="Analysis of level-specific gaps")
    strong_areas: List[StrongArea] = Field(description="Areas where candidate exceeds requirements")
    red_flags: List[RedFlag] = Field(description="Potential concerns or red flags")
    readiness_assessment: ReadinessAssessment = Field(description="Overall readiness assessment")
    
    # Summary statistics
    total_required_skills: int = Field(description="Total number of required skills from JD")
    matched_skills_count: int = Field(description="Number of skills matched")
    missing_skills_count: int = Field(description="Number of skills missing")
    match_percentage: float = Field(description="Percentage of skills matched")
    
    # Recommendations
    immediate_actions: List[str] = Field(description="Immediate actions to improve match")
    skill_development_plan: List[str] = Field(description="Skill development recommendations")
    interview_focus_areas: List[str] = Field(description="Areas to focus on during interview")
    
    # Strands Agent metadata
    status: str = "completed"
    timestamp: Optional[str] = None
    processing_time: Optional[float] = None
    agent_version: str = "1.0.0"
    
    class Config:
        use_enum_values = True
