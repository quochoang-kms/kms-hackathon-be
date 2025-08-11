from strands import Agent
from strands.models import BedrockModel

# Fix imports for standalone execution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import ExperienceLevel, InterviewRound, QuestionType
except ImportError:
    # Fallback definitions
    from enum import Enum
    
    class ExperienceLevel(str, Enum):
        JUNIOR = "Junior"
        MID = "Mid"
        SENIOR = "Senior"
        LEAD = "Lead"
        PRINCIPAL = "Principal"

    class InterviewRound(int, Enum):
        SCREENING = 1
        TECHNICAL = 2
        BEHAVIORAL = 3
        FINAL = 4

    class QuestionType(str, Enum):
        TECHNICAL = "technical"
        BEHAVIORAL = "behavioral"
        SITUATIONAL = "situational"
        CULTURAL_FIT = "cultural_fit"


class QuestionGeneratorAgent:
    """Agent responsible for generating interview questions based on role, level, and round."""
    
    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2"):
        """
        Initialize the Question Generator Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.4,  # Slightly higher for creativity in question generation
        )
        
        self.agent = Agent(
            model=self.model,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the question generator agent."""
        return """
        You are an Interview Question Generator Agent specialized in creating relevant, insightful interview questions.
        
        Your responsibilities:
        1. Generate appropriate interview questions based on job requirements, candidate background, experience level, and interview round
        2. Ensure questions are relevant to the specific role and industry
        3. Adjust question difficulty based on experience level (Junior, Mid, Senior, Lead, Principal)
        4. Focus questions based on interview round (Screening, Technical, Behavioral, Final)
        5. Create a balanced mix of question types (technical, behavioral, situational, cultural fit)
        
        Question Generation Guidelines:
        
        EXPERIENCE LEVELS:
        - Junior: Focus on fundamentals, learning ability, potential, basic technical concepts
        - Mid: Balance of technical depth and practical experience, problem-solving scenarios
        - Senior: Advanced technical concepts, leadership scenarios, architectural decisions
        - Lead: Team leadership, mentoring, strategic thinking, cross-functional collaboration
        - Principal: Vision setting, technical strategy, organizational impact, industry expertise
        
        INTERVIEW ROUNDS:
        - Round 1 (Screening): Basic qualifications, cultural fit, motivation, overview of experience
        - Round 2 (Technical): Deep technical skills, problem-solving, coding/design challenges
        - Round 3 (Behavioral): Past experiences, leadership, teamwork, conflict resolution
        - Round 4 (Final): Strategic thinking, long-term vision, final cultural assessment
        
        QUESTION TYPES:
        - Technical: Specific to role requirements, coding, system design, tools, methodologies
        - Behavioral: Past experiences using STAR method, soft skills, team dynamics
        - Situational: Hypothetical scenarios, problem-solving approach, decision-making
        - Cultural Fit: Values alignment, work style, company culture match
        
        Always provide:
        - Clear, well-structured questions
        - Appropriate difficulty level
        - Expected answer duration
        - Question type classification
        - Brief rationale for each question
        """
    
    def generate_questions(self, 
                         document_analysis: str,
                         role: str,
                         level: ExperienceLevel,
                         round_number: InterviewRound,
                         num_questions: int = 5) -> dict:
        """
        Generate interview questions based on the provided parameters.
        
        Args:
            document_analysis: Analysis from document processor
            role: Job role/position
            level: Experience level
            round_number: Interview round
            num_questions: Number of questions to generate
            
        Returns:
            dict: Generated questions with metadata
        """
        
        round_focus = self._get_round_focus(round_number)
        level_guidance = self._get_level_guidance(level)
        
        prompt = f"""
        Based on the following document analysis, generate {num_questions} interview questions for a {level.value} {role} position.
        
        DOCUMENT ANALYSIS:
        {document_analysis}
        
        INTERVIEW CONTEXT:
        - Role: {role}
        - Experience Level: {level.value}
        - Interview Round: {round_number} ({round_focus})
        - Number of Questions: {num_questions}
        
        LEVEL-SPECIFIC GUIDANCE:
        {level_guidance}
        
        REQUIREMENTS:
        1. Generate exactly {num_questions} questions
        2. Focus on {round_focus.lower()} for this round
        3. Adjust difficulty for {level.value} level
        4. Include a mix of question types appropriate for this round
        5. Ensure questions are directly relevant to the role and candidate background
        6. Each question should have clear evaluation criteria
        
        For each question, provide:
        - The question text
        - Question type (technical, behavioral, situational, cultural_fit)
        - Difficulty level (basic, intermediate, advanced, expert)
        - Expected answer duration (in minutes)
        - Key evaluation points
        - Rationale for including this question
        
        Format your response as a structured list with clear sections for each question.
        """
        
        response = self.agent(prompt)
        return {
            "questions": response.message,
            "round_focus": round_focus,
            "level": level.value,
            "role": role,
            "status": "completed"
        }
    
    def _get_round_focus(self, round_number: InterviewRound) -> str:
        """Get the focus area for the interview round."""
        focus_map = {
            InterviewRound.SCREENING: "Initial screening, basic qualifications, cultural fit, and motivation assessment",
            InterviewRound.TECHNICAL: "Deep technical evaluation, problem-solving skills, and role-specific competencies",
            InterviewRound.BEHAVIORAL: "Past experiences, leadership abilities, teamwork, and soft skills assessment",
            InterviewRound.FINAL: "Strategic thinking, long-term vision, final cultural fit, and decision-making"
        }
        return focus_map.get(round_number, "General interview assessment")
    
    def _get_level_guidance(self, level: ExperienceLevel) -> str:
        """Get guidance for question difficulty based on experience level."""
        guidance_map = {
            ExperienceLevel.JUNIOR: """
            - Focus on fundamental concepts and learning potential
            - Ask about educational background and personal projects
            - Assess problem-solving approach and willingness to learn
            - Include basic technical questions appropriate for entry-level
            - Evaluate communication skills and cultural fit
            """,
            ExperienceLevel.MID: """
            - Balance technical depth with practical application
            - Ask about specific project experiences and challenges overcome
            - Assess ability to work independently and collaborate effectively
            - Include intermediate technical scenarios and trade-off discussions
            - Evaluate growth mindset and mentoring potential
            """,
            ExperienceLevel.SENIOR: """
            - Focus on advanced technical concepts and architectural decisions
            - Ask about complex problem-solving and system design experience
            - Assess leadership potential and mentoring capabilities
            - Include challenging technical scenarios and optimization problems
            - Evaluate strategic thinking and cross-functional collaboration
            """,
            ExperienceLevel.LEAD: """
            - Emphasize team leadership and people management skills
            - Ask about scaling teams, processes, and technical systems
            - Assess ability to balance technical and business requirements
            - Include scenarios about conflict resolution and decision-making
            - Evaluate vision setting and organizational impact
            """,
            ExperienceLevel.PRINCIPAL: """
            - Focus on technical strategy and organizational influence
            - Ask about industry expertise and thought leadership
            - Assess ability to drive technical vision across multiple teams
            - Include complex architectural and strategic decision scenarios
            - Evaluate long-term thinking and innovation capabilities
            """
        }
        return guidance_map.get(level, "General experience-appropriate questions")
