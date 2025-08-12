"""Answer Evaluator Agent"""

from typing import Dict, List, Any
from strands import Agent, tool
import logging

logger = logging.getLogger(__name__)

class AnswerEvaluatorAgent(Agent):
    """Agent for generating expected answers and evaluation criteria"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @tool
    async def generate_evaluation_criteria(
        self, 
        questions: List[Dict[str, Any]], 
        level: str, 
        persona: str,
        skills_match: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate expected answers and evaluation criteria for questions
        
        Args:
            questions: List of generated questions
            level: Experience level
            persona: Interview persona
            skills_match: Skills matching analysis
            
        Returns:
            Dict with evaluation criteria and expected answers
        """
        prompt = f"""
        Create evaluation criteria and expected answer frameworks for these interview questions for a {level} level candidate:

        QUESTIONS:
        {self._format_questions_for_prompt(questions)}

        CANDIDATE PROFILE:
        - Strong Areas: {skills_match.get('strong_areas', [])}
        - Missing Skills: {skills_match.get('missing_skills', [])}
        - Match Score: {skills_match.get('overall_match_score', 0)}%

        For each question, provide:
        1. Expected answer key points (level-appropriate for {level})
        2. Evaluation criteria (what to look for)
        3. Scoring rubric (1-5 scale with descriptions)
        4. Level-specific expectations
        5. Red flags to watch for
        6. Follow-up question suggestions
        7. STAR method criteria (for behavioral questions)
        8. Persona-specific evaluation approach for {persona} style

        Focus on {level}-level competencies and expectations.
        """
        
        try:
            result = await self.invoke_async(prompt)
            response = str(result)
            
            # Parse the response
            evaluations = self._parse_evaluation_criteria(response, questions, level, persona)
            
            return {
                "level": level,
                "persona": persona,
                "total_questions": len(questions),
                "evaluations": evaluations,
                "raw_response": response
            }
            
        except Exception as e:
            logger.error(f"Evaluation criteria generation failed: {str(e)}")
            return {
                "level": level,
                "persona": persona,
                "error": str(e),
                "evaluations": []
            }
    
    def _format_questions_for_prompt(self, questions: List[Dict[str, Any]]) -> str:
        """Format questions for the prompt"""
        formatted = []
        for i, q in enumerate(questions, 1):
            formatted.append(f"{i}. {q.get('text', '')} (Type: {q.get('question_type', 'General')})")
        return '\n'.join(formatted)
    
    def _parse_evaluation_criteria(
        self, 
        response_text: str, 
        questions: List[Dict[str, Any]], 
        level: str, 
        persona: str
    ) -> List[Dict[str, Any]]:
        """Parse evaluation criteria from LLM response"""
        evaluations = []
        
        # Simple parsing - in production, use more sophisticated parsing
        sections = response_text.split('\n\n')
        
        for i, question in enumerate(questions):
            evaluation = {
                "question_id": i + 1,
                "question_text": question.get('text', ''),
                "question_type": question.get('question_type', 'General'),
                "expected_answer_points": self._extract_expected_points(response_text, i + 1),
                "evaluation_criteria": self._extract_evaluation_criteria(response_text, i + 1),
                "scoring_rubric": self._create_scoring_rubric(level, question.get('question_type', 'General')),
                "level_expectations": self._get_level_expectations(level, question.get('question_type', 'General')),
                "red_flags": self._extract_red_flags(response_text, i + 1),
                "follow_up_questions": self._extract_follow_ups(response_text, i + 1),
                "star_criteria": self._get_star_criteria(question.get('question_type', 'General')),
                "persona_approach": self._get_persona_evaluation_approach(persona)
            }
            evaluations.append(evaluation)
        
        return evaluations
    
    def _extract_expected_points(self, text: str, question_num: int) -> List[str]:
        """Extract expected answer points for a question"""
        # Simple extraction - look for bullet points near question number
        lines = text.split('\n')
        points = []
        
        in_expected_section = False
        for line in lines:
            if f"Question {question_num}" in line or f"{question_num}." in line:
                in_expected_section = True
                continue
            elif f"Question {question_num + 1}" in line or f"{question_num + 1}." in line:
                break
            elif in_expected_section and (line.strip().startswith('-') or line.strip().startswith('•')):
                points.append(line.strip()[1:].strip())
        
        return points[:5]  # Limit to 5 key points
    
    def _extract_evaluation_criteria(self, text: str, question_num: int) -> List[str]:
        """Extract evaluation criteria for a question"""
        # Similar extraction logic
        return [
            "Clarity and structure of response",
            "Depth of technical knowledge",
            "Relevant examples and experience",
            "Communication skills"
        ]
    
    def _create_scoring_rubric(self, level: str, question_type: str) -> Dict[str, str]:
        """Create scoring rubric based on level and question type"""
        base_rubric = {
            "5": "Exceptional - Exceeds expectations significantly",
            "4": "Strong - Meets expectations with additional insights",
            "3": "Satisfactory - Meets basic expectations",
            "2": "Below Average - Partially meets expectations",
            "1": "Poor - Does not meet expectations"
        }
        
        # Customize based on level
        if level in ["Senior", "Lead", "Principal"]:
            base_rubric["5"] = f"Exceptional - Demonstrates {level}-level expertise and leadership"
            base_rubric["4"] = f"Strong - Shows solid {level}-level competencies"
        
        return base_rubric
    
    def _get_level_expectations(self, level: str, question_type: str) -> str:
        """Get level-specific expectations"""
        expectations = {
            "Junior": "Basic understanding, willingness to learn, potential for growth",
            "Mid": "Solid technical skills, some leadership experience, independent work",
            "Senior": "Advanced expertise, mentoring others, architectural thinking",
            "Lead": "Team leadership, strategic thinking, cross-functional collaboration",
            "Principal": "Vision setting, technical strategy, organizational impact"
        }
        return expectations.get(level, expectations["Mid"])
    
    def _extract_red_flags(self, text: str, question_num: int) -> List[str]:
        """Extract red flags to watch for"""
        return [
            "Inability to provide specific examples",
            "Lack of technical depth for the level",
            "Poor communication skills",
            "Negative attitude toward previous roles"
        ]
    
    def _extract_follow_ups(self, text: str, question_num: int) -> List[str]:
        """Extract follow-up question suggestions"""
        return [
            "Can you provide a specific example?",
            "How would you handle this differently now?",
            "What did you learn from that experience?"
        ]
    
    def _get_star_criteria(self, question_type: str) -> Dict[str, str]:
        """Get STAR method criteria for behavioral questions"""
        if question_type == "Behavioral":
            return {
                "Situation": "Clear context and background",
                "Task": "Specific responsibility or challenge",
                "Action": "Concrete steps taken",
                "Result": "Measurable outcomes and learning"
            }
        return {}
    
    def _get_persona_evaluation_approach(self, persona: str) -> str:
        """Get persona-specific evaluation approach"""
        approaches = {
            "Friendly": "Focus on potential and growth mindset, encourage elaboration",
            "Serious": "Strict adherence to criteria, objective assessment",
            "Analytical": "Deep dive into technical details, probe for understanding",
            "Collaborative": "Assess teamwork and partnership skills",
            "Challenging": "Test resilience and problem-solving under pressure"
        }
        return approaches.get(persona, approaches["Friendly"])