"""Question Generator Agent"""

from typing import Dict, List, Any
from strands import Agent, tool
import logging

logger = logging.getLogger(__name__)

class QuestionGeneratorAgent(Agent):
    """Agent for generating interview questions based on analysis and parameters"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @tool
    async def generate_questions(
        self, 
        skills_match: Dict[str, Any], 
        level: str, 
        round_number: int, 
        persona: str,
        role: str
    ) -> Dict[str, Any]:
        """Generate interview questions based on analysis and parameters
        
        Args:
            skills_match: Skills matching analysis results
            level: Experience level (Junior, Mid, Senior, Lead, Principal)
            round_number: Interview round (1-4)
            persona: Interview persona (Friendly, Serious, etc.)
            role: Target role
            
        Returns:
            Dict with generated questions
        """
        round_names = {1: "Screening", 2: "Technical", 3: "Behavioral", 4: "Final"}
        round_name = round_names.get(round_number, "General")
        
        # Level-specific guidelines
        level_guidelines = self._get_level_guidelines(level)
        
        # Round-specific focus
        round_focus = self._get_round_focus(round_number)
        
        # Persona styling
        persona_style = self._get_persona_style(persona)
        
        prompt = f"""
        Generate interview questions for a {level} {role} candidate in Round {round_number} ({round_name}) with {persona} persona.

        CANDIDATE ANALYSIS:
        - Matched Skills: {skills_match.get('matched_skills', [])}
        - Missing Skills: {skills_match.get('missing_skills', [])}
        - Strong Areas: {skills_match.get('strong_areas', [])}
        - Red Flags: {skills_match.get('red_flags', [])}
        - Overall Match Score: {skills_match.get('overall_match_score', 0)}%

        LEVEL GUIDELINES ({level}):
        {level_guidelines}

        ROUND FOCUS ({round_name}):
        {round_focus}

        PERSONA STYLE ({persona}):
        {persona_style}

        Generate 8-12 questions with:
        1. Question text
        2. Question type (Technical, Behavioral, Situational, Cultural Fit)
        3. Difficulty level (1-5)
        4. Round alignment score (1-5)
        5. Persona style application
        6. Focus areas based on candidate's profile

        Ensure questions are:
        - Level-appropriate for {level}
        - Round-specific for {round_name}
        - Styled according to {persona} persona
        - Tailored to candidate's strengths and gaps
        """
        
        try:
            result = await self.invoke_async(prompt)
            response = str(result)
            
            # Parse the response
            questions = self._parse_questions(response, level, round_number, persona)
            
            return {
                "level": level,
                "round_number": round_number,
                "round_name": round_name,
                "persona": persona,
                "role": role,
                "questions": questions,
                "total_questions": len(questions),
                "raw_response": response
            }
            
        except Exception as e:
            logger.error(f"Question generation failed: {str(e)}")
            return {
                "level": level,
                "round_number": round_number,
                "persona": persona,
                "error": str(e),
                "questions": []
            }
    
    def _get_level_guidelines(self, level: str) -> str:
        """Get level-specific guidelines"""
        guidelines = {
            "Junior": "Focus on fundamentals, learning ability, potential, basic technical concepts, eagerness to learn",
            "Mid": "Balance technical depth with practical experience, problem-solving scenarios, independent work capability",
            "Senior": "Advanced technical concepts, leadership scenarios, architectural decisions, mentoring others",
            "Lead": "Team leadership, mentoring capabilities, strategic thinking, cross-functional collaboration",
            "Principal": "Vision setting, technical strategy, organizational impact, industry expertise, thought leadership"
        }
        return guidelines.get(level, guidelines["Mid"])
    
    def _get_round_focus(self, round_number: int) -> str:
        """Get round-specific focus areas"""
        focus = {
            1: "Basic qualifications, cultural fit, motivation assessment, overview of experience, initial screening",
            2: "Deep technical evaluation, problem-solving, hands-on challenges, coding/design skills, technical depth",
            3: "STAR method questions, leadership examples, team dynamics, past experiences, behavioral competencies",
            4: "Strategic thinking, long-term vision, comprehensive cultural assessment, final decision factors"
        }
        return focus.get(round_number, focus[2])
    
    def _get_persona_style(self, persona: str) -> str:
        """Get persona-specific styling guidelines"""
        styles = {
            "Friendly": "Warm tone, encouraging language, supportive questioning style, puts candidate at ease",
            "Serious": "Professional approach, direct questions, competency-focused assessment, formal tone",
            "Analytical": "Detail-oriented questions, probing follow-ups, deep understanding focus, methodical approach",
            "Collaborative": "Team-oriented questions, partnership emphasis, cooperation assessment, inclusive language",
            "Challenging": "Boundary-pushing questions, resilience testing, pressure scenarios, rigorous evaluation"
        }
        return styles.get(persona, styles["Friendly"])
    
    def _parse_questions(self, response_text: str, level: str, round_number: int, persona: str) -> List[Dict[str, Any]]:
        """Parse generated questions from LLM response"""
        questions = []
        lines = response_text.split('\n')
        
        current_question = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for question patterns
            if line.startswith('Q') or line.startswith('Question') or line.endswith('?'):
                # Save previous question if exists
                if current_question.get('text'):
                    questions.append(current_question)
                
                # Start new question
                current_question = {
                    'text': line,
                    'question_type': 'Technical',  # Default
                    'difficulty_level': 3,  # Default
                    'round_alignment': round_number,
                    'persona_style': persona,
                    'level': level
                }
            elif 'type:' in line.lower():
                q_type = line.split(':', 1)[1].strip()
                current_question['question_type'] = q_type
            elif 'difficulty:' in line.lower():
                try:
                    difficulty = int(line.split(':', 1)[1].strip().split()[0])
                    current_question['difficulty_level'] = min(5, max(1, difficulty))
                except:
                    pass
        
        # Add the last question
        if current_question.get('text'):
            questions.append(current_question)
        
        # If parsing failed, create default questions
        if not questions:
            questions = self._create_default_questions(level, round_number, persona)
        
        return questions[:12]  # Limit to 12 questions
    
    def _create_default_questions(self, level: str, round_number: int, persona: str) -> List[Dict[str, Any]]:
        """Create default questions if parsing fails"""
        default_questions = [
            {
                'text': f"Tell me about your experience relevant to this {level} position.",
                'question_type': 'Behavioral',
                'difficulty_level': 2,
                'round_alignment': round_number,
                'persona_style': persona,
                'level': level
            },
            {
                'text': "What interests you most about this role?",
                'question_type': 'Cultural Fit',
                'difficulty_level': 1,
                'round_alignment': round_number,
                'persona_style': persona,
                'level': level
            }
        ]
        return default_questions