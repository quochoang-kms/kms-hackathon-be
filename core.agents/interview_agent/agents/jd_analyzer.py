"""Job Description Analyzer Agent"""

from typing import Dict, List, Any
from strands_agents import Agent, tool
import logging

logger = logging.getLogger(__name__)

class JDAnalyzerAgent(Agent):
    """Agent for analyzing job descriptions and extracting requirements"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @tool
    async def analyze_job_description(self, jd_text: str, role: str, level: str) -> Dict[str, Any]:
        """Analyze job description and extract key requirements
        
        Args:
            jd_text: Job description text content
            role: Target role (e.g., "Software Engineer")
            level: Experience level (Junior, Mid, Senior, Lead, Principal)
            
        Returns:
            Dict with extracted requirements and skills
        """
        prompt = f"""
        Analyze this job description for a {level} {role} position and extract:

        1. Required technical skills (must-have)
        2. Preferred technical skills (nice-to-have)
        3. Soft skills and competencies
        4. Experience requirements
        5. Education requirements
        6. Level-specific competencies for {level} level
        7. Key responsibilities

        Job Description:
        {jd_text}

        Provide a structured analysis focusing on {level}-level expectations.
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            
            # Parse the response to extract structured data
            analysis = self._parse_jd_analysis(response.content, level)
            
            return {
                "role": role,
                "level": level,
                "required_skills": analysis.get("required_skills", []),
                "preferred_skills": analysis.get("preferred_skills", []),
                "soft_skills": analysis.get("soft_skills", []),
                "experience_requirements": analysis.get("experience_requirements", ""),
                "education_requirements": analysis.get("education_requirements", ""),
                "level_competencies": analysis.get("level_competencies", []),
                "key_responsibilities": analysis.get("key_responsibilities", []),
                "raw_analysis": response.content
            }
            
        except Exception as e:
            logger.error(f"JD analysis failed: {str(e)}")
            return {
                "role": role,
                "level": level,
                "error": str(e),
                "required_skills": [],
                "preferred_skills": [],
                "soft_skills": []
            }
    
    def _parse_jd_analysis(self, analysis_text: str, level: str) -> Dict[str, Any]:
        """Parse the LLM analysis response into structured data"""
        # Simple parsing - in production, use more sophisticated parsing
        lines = analysis_text.split('\n')
        
        result = {
            "required_skills": [],
            "preferred_skills": [],
            "soft_skills": [],
            "experience_requirements": "",
            "education_requirements": "",
            "level_competencies": [],
            "key_responsibilities": []
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if "required" in line.lower() and "skill" in line.lower():
                current_section = "required_skills"
            elif "preferred" in line.lower() and "skill" in line.lower():
                current_section = "preferred_skills"
            elif "soft skill" in line.lower():
                current_section = "soft_skills"
            elif "experience" in line.lower():
                current_section = "experience_requirements"
            elif "education" in line.lower():
                current_section = "education_requirements"
            elif "competenc" in line.lower():
                current_section = "level_competencies"
            elif "responsibilit" in line.lower():
                current_section = "key_responsibilities"
            elif line.startswith('-') or line.startswith('•'):
                # Extract list items
                item = line[1:].strip()
                if current_section and current_section in ["required_skills", "preferred_skills", "soft_skills", "level_competencies", "key_responsibilities"]:
                    result[current_section].append(item)
            elif current_section in ["experience_requirements", "education_requirements"]:
                result[current_section] += line + " "
        
        return result