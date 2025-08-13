"""CV Analyzer Agent"""

from typing import Dict, List, Any
from strands import Agent, tool
import logging

logger = logging.getLogger(__name__)

class CVAnalyzerAgent(Agent):
    """Agent for analyzing candidate CVs and extracting skills and experience"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @tool
    async def analyze_cv(self, cv_text: str, target_role: str, target_level: str) -> Dict[str, Any]:
        """Analyze CV and extract candidate information
        
        Args:
            cv_text: CV text content
            target_role: Target role for comparison
            target_level: Target experience level
            
        Returns:
            Dict with extracted candidate information
        """
        prompt = f"""
        Analyze this CV for a candidate applying for a {target_level} {target_role} position:

        1. Extract technical skills and proficiency levels
        2. Identify work experience and career progression
        3. Extract education background
        4. Identify leadership and mentoring experience (especially for Senior+ levels)
        5. Assess experience level alignment with {target_level} expectations
        6. Identify key achievements and projects
        7. Extract soft skills demonstrated through experience

        CV Content:
        {cv_text}

        Focus on assessing readiness for {target_level} level responsibilities.
        """
        
        try:
            result = await self.invoke_async(prompt)
            response = str(result)
            
            # Parse the response to extract structured data
            analysis = self._parse_cv_analysis(response, target_level)
            
            return {
                "target_role": target_role,
                "target_level": target_level,
                "technical_skills": analysis.get("technical_skills", []),
                "work_experience": analysis.get("work_experience", []),
                "education": analysis.get("education", []),
                "leadership_experience": analysis.get("leadership_experience", []),
                "level_alignment": analysis.get("level_alignment", ""),
                "key_achievements": analysis.get("key_achievements", []),
                "demonstrated_soft_skills": analysis.get("demonstrated_soft_skills", []),
                "years_of_experience": analysis.get("years_of_experience", 0),
                "raw_analysis": response
            }
            
        except Exception as e:
            logger.error(f"CV analysis failed: {str(e)}")
            return {
                "target_role": target_role,
                "target_level": target_level,
                "error": str(e),
                "technical_skills": [],
                "work_experience": [],
                "education": []
            }
    
    def _parse_cv_analysis(self, analysis_text: str, target_level: str) -> Dict[str, Any]:
        """Parse the LLM analysis response into structured data"""
        lines = analysis_text.split('\n')
        
        result = {
            "technical_skills": [],
            "work_experience": [],
            "education": [],
            "leadership_experience": [],
            "level_alignment": "",
            "key_achievements": [],
            "demonstrated_soft_skills": [],
            "years_of_experience": 0
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if "technical skill" in line.lower():
                current_section = "technical_skills"
            elif "work experience" in line.lower() or "experience" in line.lower():
                current_section = "work_experience"
            elif "education" in line.lower():
                current_section = "education"
            elif "leadership" in line.lower():
                current_section = "leadership_experience"
            elif "alignment" in line.lower():
                current_section = "level_alignment"
            elif "achievement" in line.lower():
                current_section = "key_achievements"
            elif "soft skill" in line.lower():
                current_section = "demonstrated_soft_skills"
            elif line.startswith('-') or line.startswith('•'):
                # Extract list items
                item = line[1:].strip()
                if current_section and current_section in ["technical_skills", "work_experience", "education", "leadership_experience", "key_achievements", "demonstrated_soft_skills"]:
                    result[current_section].append(item)
            elif current_section == "level_alignment":
                result[current_section] += line + " "
        
        # Try to extract years of experience
        import re
        years_match = re.search(r'(\d+)\s*years?\s*of\s*experience', analysis_text.lower())
        if years_match:
            result["years_of_experience"] = int(years_match.group(1))
        
        return result