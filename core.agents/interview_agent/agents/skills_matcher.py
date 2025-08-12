"""Skills Matcher Agent"""

from typing import Dict, List, Any, Tuple
from strands import Agent, tool
import logging

logger = logging.getLogger(__name__)

class SkillsMatcherAgent(Agent):
    """Agent for matching JD requirements against CV skills"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @tool
    async def match_skills(self, jd_analysis: Dict[str, Any], cv_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Match CV skills against JD requirements
        
        Args:
            jd_analysis: Job description analysis results
            cv_analysis: CV analysis results
            
        Returns:
            Dict with matching results and gap analysis
        """
        level = jd_analysis.get("level", "Mid")
        
        prompt = f"""
        Compare the candidate's skills and experience against the job requirements for a {level} level position:

        JOB REQUIREMENTS:
        Required Skills: {jd_analysis.get('required_skills', [])}
        Preferred Skills: {jd_analysis.get('preferred_skills', [])}
        Level Competencies: {jd_analysis.get('level_competencies', [])}
        
        CANDIDATE PROFILE:
        Technical Skills: {cv_analysis.get('technical_skills', [])}
        Experience Level: {cv_analysis.get('years_of_experience', 0)} years
        Leadership Experience: {cv_analysis.get('leadership_experience', [])}
        
        Provide:
        1. Matched skills with confidence scores (0-100)
        2. Missing critical skills with impact assessment
        3. Level-specific skill gap analysis for {level} position
        4. Strong areas where candidate exceeds requirements
        5. Potential red flags or concerns
        6. Overall readiness assessment for {level} level
        """
        
        try:
            result = await self.invoke_async(prompt)
            response = str(result)
            
            # Parse the response
            analysis = self._parse_matching_analysis(response, jd_analysis, cv_analysis)
            
            return {
                "level": level,
                "matched_skills": analysis.get("matched_skills", []),
                "missing_skills": analysis.get("missing_skills", []),
                "strong_areas": analysis.get("strong_areas", []),
                "red_flags": analysis.get("red_flags", []),
                "level_readiness": analysis.get("level_readiness", ""),
                "overall_match_score": analysis.get("overall_match_score", 0),
                "raw_analysis": response
            }
            
        except Exception as e:
            logger.error(f"Skills matching failed: {str(e)}")
            return {
                "level": level,
                "error": str(e),
                "matched_skills": [],
                "missing_skills": [],
                "strong_areas": [],
                "red_flags": []
            }
    
    def _parse_matching_analysis(self, analysis_text: str, jd_analysis: Dict, cv_analysis: Dict) -> Dict[str, Any]:
        """Parse the matching analysis response"""
        lines = analysis_text.split('\n')
        
        result = {
            "matched_skills": [],
            "missing_skills": [],
            "strong_areas": [],
            "red_flags": [],
            "level_readiness": "",
            "overall_match_score": 0
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if "matched skill" in line.lower():
                current_section = "matched_skills"
            elif "missing" in line.lower() and "skill" in line.lower():
                current_section = "missing_skills"
            elif "strong" in line.lower():
                current_section = "strong_areas"
            elif "red flag" in line.lower() or "concern" in line.lower():
                current_section = "red_flags"
            elif "readiness" in line.lower():
                current_section = "level_readiness"
            elif line.startswith('-') or line.startswith('•'):
                # Extract list items
                item = line[1:].strip()
                if current_section and current_section in ["matched_skills", "missing_skills", "strong_areas", "red_flags"]:
                    # Try to extract confidence scores for matched skills
                    if current_section == "matched_skills":
                        import re
                        score_match = re.search(r'(\d+)%?', item)
                        score = int(score_match.group(1)) if score_match else 50
                        skill_name = re.sub(r'\s*\(\d+%?\)', '', item).strip()
                        result[current_section].append({
                            "skill": skill_name,
                            "confidence": score
                        })
                    else:
                        result[current_section].append(item)
            elif current_section == "level_readiness":
                result[current_section] += line + " "
        
        # Calculate overall match score
        if result["matched_skills"]:
            total_score = sum(skill.get("confidence", 0) for skill in result["matched_skills"])
            result["overall_match_score"] = total_score // len(result["matched_skills"])
        
        return result