from pydantic import BaseModel
from typing import Optional
from .jd_response import JDResponse
from .cv_response import CVResponse
from .skill_matcher_response import SkillMatcherResponse

class SkillAnalysisResponse(BaseModel):
    status: str
    execution_time: Optional[float] = None
    timestamp: Optional[str] = None
    jd_analysis: Optional[JDResponse] = None
    cv_analysis: Optional[CVResponse] = None
    skill_matching: Optional[SkillMatcherResponse] = None
    analysis_summary: Optional[dict] = None