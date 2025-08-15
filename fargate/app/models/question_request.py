from pydantic import BaseModel
from typing import Optional, Dict, Any
from .jd_response import JDResponse
from .cv_response import CVResponse
from .skill_matcher_response import SkillMatcherResponse

class QuestionGenerationRequest(BaseModel):
    jd_analysis: JDResponse
    cv_analysis: CVResponse
    skill_matching: SkillMatcherResponse
    additional_context: Optional[str] = None

class QuestionGenerationResponse(BaseModel):
    status: str
    execution_time: Optional[float] = None
    timestamp: Optional[str] = None
    questions: Optional[Dict[str, Any]] = None