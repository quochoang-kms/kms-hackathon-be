from strands import Agent
from strands.models import BedrockModel

# Fix imports for standalone execution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import ExperienceLevel, InterviewRound
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


class AnswerTipsGeneratorAgent:
    """Agent responsible for generating evaluation tips and criteria for interviewers to assess candidate responses."""
    
    def __init__(self, model_id: str = "apac.anthropic.claude-sonnet-4-20250514-v1:0", region: str = "ap-southeast-1"):
        """
        Initialize the Answer Tips Generator Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.2,  # Lower temperature for consistent evaluation criteria
        )
        
        self.agent = Agent(
            model=self.model,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the answer tips generator agent."""
        return """
        You are an Interview Evaluation Tips Generator Agent specialized in helping interviewers assess candidate responses effectively.
        
        Your responsibilities:
        1. Generate comprehensive evaluation criteria for each interview question
        2. Provide specific tips on what to listen for in candidate responses
        3. Identify key indicators of strong vs. weak answers
        4. Suggest follow-up questions to probe deeper
        5. Highlight red flags and excellent response indicators
        6. Provide scoring guidelines and assessment frameworks
        
        Evaluation Tips Guidelines:
        
        FOR BEHAVIORAL QUESTIONS:
        - Look for STAR method usage (Situation, Task, Action, Result)
        - Assess specificity and measurable outcomes
        - Evaluate leadership, problem-solving, and collaboration skills
        - Check for learning mindset and growth examples
        - Listen for ownership and accountability
        
        FOR TECHNICAL QUESTIONS:
        - Evaluate technical accuracy and depth
        - Assess problem-solving approach and methodology
        - Look for understanding of trade-offs and alternatives
        - Check for practical experience indicators
        - Listen for best practices and industry knowledge
        
        FOR SITUATIONAL QUESTIONS:
        - Assess structured thinking and problem-solving process
        - Look for stakeholder consideration and impact analysis
        - Evaluate decision-making framework
        - Check for risk assessment capabilities
        - Listen for adaptability and flexibility
        
        FOR CULTURAL FIT QUESTIONS:
        - Assess alignment with company values
        - Look for collaboration and teamwork examples
        - Evaluate communication style and professionalism
        - Check for adaptability and learning orientation
        - Listen for passion and motivation indicators
        
        EVALUATION FRAMEWORK:
        For each question, provide:
        
        1. **What to Listen For**: Key elements of a strong response
        2. **Scoring Criteria**: 1-5 scale with specific indicators
        3. **Red Flags**: Warning signs of poor fit or capability
        4. **Excellent Indicators**: Signs of exceptional candidates
        5. **Follow-up Questions**: Probing questions to dig deeper
        6. **Assessment Notes**: What to document during the interview
        
        RESPONSE QUALITY INDICATORS:
        
        STRONG RESPONSES:
        - Specific, concrete examples with measurable results
        - Clear structure and logical flow
        - Demonstrates relevant skills and experience
        - Shows self-awareness and learning from mistakes
        - Indicates cultural fit and values alignment
        
        WEAK RESPONSES:
        - Vague or generic answers without specifics
        - Lack of structure or rambling responses
        - No concrete examples or measurable outcomes
        - Blame others without taking responsibility
        - Misalignment with role requirements or company culture
        
        Always provide practical, actionable guidance that helps interviewers make informed decisions while maintaining fairness and objectivity.
        """
    
    async def generate_answer_tips(self, questions: list, context: dict) -> list:
        """
        Generate evaluation tips for a list of interview questions.
        
        Args:
            questions: List of interview questions with metadata
            context: Interview context (role, level, round, etc.)
            
        Returns:
            List of evaluation tips for each question
        """
        role = context.get('role', 'Unknown Role')
        level = context.get('level', ExperienceLevel.MID)
        round_number = context.get('round_number', InterviewRound.TECHNICAL)
        
        # Create context for the agent
        context_prompt = f"""
        Interview Context:
        - Role: {role}
        - Experience Level: {level.value if hasattr(level, 'value') else level}
        - Interview Round: {round_number.value if hasattr(round_number, 'value') else round_number}
        
        Generate comprehensive evaluation tips for the following interview questions.
        For each question, provide detailed guidance on how to assess candidate responses.
        """
        
        answer_tips = []
        
        for question_data in questions:
            question = question_data.get('question', '')
            question_type = question_data.get('type', 'general')
            difficulty = question_data.get('difficulty', 'intermediate')
            
            prompt = f"""
            {context_prompt}
            
            Question: {question}
            Type: {question_type}
            Difficulty: {difficulty}
            
            Please provide comprehensive evaluation tips for this question including:
            
            1. **What to Listen For**: Key elements of a strong response
            2. **Scoring Criteria**: Detailed 1-5 scale with specific indicators
            3. **Red Flags**: Warning signs to watch out for
            4. **Excellent Indicators**: Signs of exceptional responses
            5. **Follow-up Questions**: 2-3 probing questions to dig deeper
            6. **Assessment Framework**: How to structure your evaluation
            7. **Time Management**: Expected response length and pacing
            
            Format your response as a structured evaluation guide that an interviewer can reference during the interview.
            """
            
            try:
                response = await self.agent.run(prompt)
                
                answer_tips.append({
                    'question': question,
                    'question_type': question_type,
                    'difficulty': difficulty,
                    'evaluation_tips': response,
                    'what_to_listen_for': self._extract_section(response, 'What to Listen For'),
                    'scoring_criteria': self._extract_section(response, 'Scoring Criteria'),
                    'red_flags': self._extract_section(response, 'Red Flags'),
                    'excellent_indicators': self._extract_section(response, 'Excellent Indicators'),
                    'follow_up_questions': self._extract_section(response, 'Follow-up Questions'),
                    'assessment_framework': self._extract_section(response, 'Assessment Framework'),
                    'time_management': self._extract_section(response, 'Time Management')
                })
                
            except Exception as e:
                print(f"Error generating answer tips for question: {e}")
                # Provide fallback tips
                answer_tips.append({
                    'question': question,
                    'question_type': question_type,
                    'difficulty': difficulty,
                    'evaluation_tips': f"Evaluate candidate's response for relevance, specificity, and alignment with {role} requirements.",
                    'what_to_listen_for': ["Specific examples", "Relevant experience", "Problem-solving approach"],
                    'scoring_criteria': "Rate 1-5 based on relevance, depth, and clarity of response",
                    'red_flags': ["Vague answers", "Lack of examples", "Inconsistencies"],
                    'excellent_indicators': ["Concrete examples", "Measurable results", "Clear methodology"],
                    'follow_up_questions': ["Can you provide more details?", "What was the outcome?", "How did you measure success?"],
                    'assessment_framework': "Structure, Content, Delivery, Relevance",
                    'time_management': "2-4 minutes expected response time"
                })
        
        return answer_tips
    
    def _extract_section(self, response: str, section_name: str) -> str:
        """Extract a specific section from the response."""
        try:
            lines = response.split('\n')
            section_content = []
            in_section = False
            
            for line in lines:
                if section_name.lower() in line.lower() and ('**' in line or '#' in line or ':' in line):
                    in_section = True
                    continue
                elif in_section and ('**' in line or line.startswith('#')) and section_name.lower() not in line.lower():
                    break
                elif in_section:
                    section_content.append(line.strip())
            
            return '\n'.join(section_content).strip() if section_content else f"Assess {section_name.lower()} for this question type."
            
        except Exception:
            return f"Evaluate {section_name.lower()} based on question requirements."
    
    def generate_answer_tips_sync(self, questions: list, context: dict) -> list:
        """
        Synchronous wrapper for generate_answer_tips.
        
        Args:
            questions: List of interview questions with metadata
            context: Interview context
            
        Returns:
            List of evaluation tips for each question
        """
        import asyncio
        return asyncio.run(self.generate_answer_tips(questions, context))
    
    def get_general_evaluation_framework(self, role: str, level: ExperienceLevel) -> dict:
        """
        Get a general evaluation framework for the role and level.
        
        Args:
            role: Job role
            level: Experience level
            
        Returns:
            General evaluation framework
        """
        return {
            'overall_assessment_criteria': [
                'Technical competency',
                'Problem-solving ability',
                'Communication skills',
                'Cultural fit',
                'Leadership potential',
                'Learning agility'
            ],
            'scoring_scale': {
                '5': 'Exceptional - Exceeds expectations significantly',
                '4': 'Strong - Meets expectations with some excellence',
                '3': 'Good - Meets basic expectations',
                '2': 'Below Average - Some concerns or gaps',
                '1': 'Poor - Significant concerns or misalignment'
            },
            'level_expectations': {
                ExperienceLevel.JUNIOR: 'Focus on potential, learning ability, and foundational skills',
                ExperienceLevel.MID: 'Balance of technical skills and some leadership/mentoring capability',
                ExperienceLevel.SENIOR: 'Strong technical expertise with leadership and strategic thinking',
                ExperienceLevel.LEAD: 'Technical leadership, team management, and strategic planning',
                ExperienceLevel.PRINCIPAL: 'Technical vision, organizational impact, and thought leadership'
            }.get(level, 'Assess based on role requirements'),
            'interview_best_practices': [
                'Take detailed notes during responses',
                'Ask follow-up questions for clarity',
                'Look for specific examples and measurable results',
                'Assess both technical and soft skills',
                'Consider cultural fit and values alignment',
                'Be consistent in evaluation criteria across candidates'
            ]
        }
