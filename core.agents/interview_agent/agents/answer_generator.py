from strands import Agent
from strands.models import BedrockModel
from ..models import ExperienceLevel, InterviewRound


class AnswerGeneratorAgent:
    """Agent responsible for generating sample answers to interview questions."""
    
    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2"):
        """
        Initialize the Answer Generator Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.3,  # Lower temperature for consistent, high-quality answers
        )
        
        self.agent = Agent(
            model=self.model,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the answer generator agent."""
        return """
        You are an Interview Answer Generator Agent specialized in creating high-quality sample answers for interview questions.
        
        Your responsibilities:
        1. Generate comprehensive, well-structured sample answers for interview questions
        2. Ensure answers are appropriate for the experience level and role
        3. Use proven frameworks like STAR (Situation, Task, Action, Result) for behavioral questions
        4. Provide technical answers with appropriate depth and accuracy
        5. Include key evaluation criteria for interviewers
        6. Demonstrate best practices and industry standards
        
        Answer Generation Guidelines:
        
        BEHAVIORAL QUESTIONS:
        - Use STAR method (Situation, Task, Action, Result)
        - Include specific, measurable outcomes
        - Show leadership, problem-solving, and collaboration skills
        - Demonstrate learning and growth mindset
        
        TECHNICAL QUESTIONS:
        - Provide accurate, up-to-date technical information
        - Show depth appropriate to experience level
        - Include trade-offs and alternative approaches
        - Demonstrate practical experience and best practices
        
        SITUATIONAL QUESTIONS:
        - Show structured problem-solving approach
        - Consider multiple perspectives and stakeholders
        - Demonstrate decision-making process
        - Include risk assessment and mitigation strategies
        
        CULTURAL FIT QUESTIONS:
        - Align with common positive workplace values
        - Show adaptability and collaboration
        - Demonstrate professional growth orientation
        - Include specific examples and experiences
        
        ANSWER QUALITY STANDARDS:
        - Clear, concise, and well-organized
        - Specific examples with quantifiable results
        - Professional tone and language
        - Appropriate length (2-4 minutes speaking time)
        - Actionable insights for interviewers
        
        For each answer, also provide:
        - Key points the candidate should cover
        - What interviewers should listen for
        - Red flags or concerning responses
        - Follow-up questions to consider
        """
    
    def generate_answers(self,
                        questions: str,
                        document_analysis: str,
                        role: str,
                        level: ExperienceLevel,
                        round_number: InterviewRound) -> dict:
        """
        Generate sample answers for the provided interview questions.
        
        Args:
            questions: Generated interview questions
            document_analysis: Analysis from document processor
            role: Job role/position
            level: Experience level
            round_number: Interview round
            
        Returns:
            dict: Generated sample answers with evaluation criteria
        """
        
        level_context = self._get_level_context(level)
        round_context = self._get_round_context(round_number)
        
        prompt = f"""
        Generate comprehensive sample answers for the following interview questions for a {level.value} {role} position.
        
        INTERVIEW QUESTIONS:
        {questions}
        
        DOCUMENT ANALYSIS CONTEXT:
        {document_analysis}
        
        POSITION CONTEXT:
        - Role: {role}
        - Experience Level: {level.value}
        - Interview Round: {round_number}
        
        LEVEL-SPECIFIC CONTEXT:
        {level_context}
        
        ROUND-SPECIFIC CONTEXT:
        {round_context}
        
        REQUIREMENTS:
        1. Generate a high-quality sample answer for each question
        2. Ensure answers are appropriate for the {level.value} experience level
        3. Use relevant frameworks (STAR for behavioral, structured approach for technical)
        4. Include specific, realistic examples that align with the role
        5. Demonstrate the skills and experience expected at this level
        6. Keep answers concise but comprehensive (2-4 minutes speaking time)
        
        For each answer, provide:
        - The complete sample answer
        - Key points that should be covered
        - Evaluation criteria for interviewers
        - What makes this a strong answer
        - Potential follow-up questions
        - Red flags if the candidate's actual answer differs significantly
        
        Structure your response clearly with sections for each question and its corresponding answer analysis.
        """
        
        response = self.agent(prompt)
        return {
            "sample_answers": response.message,
            "level": level.value,
            "role": role,
            "round": round_number,
            "status": "completed"
        }
    
    def _get_level_context(self, level: ExperienceLevel) -> str:
        """Get context for answer generation based on experience level."""
        context_map = {
            ExperienceLevel.JUNIOR: """
            - Answers should show enthusiasm for learning and growth
            - Focus on educational projects, internships, and personal initiatives
            - Demonstrate foundational knowledge and problem-solving approach
            - Show willingness to ask questions and seek mentorship
            - Include examples of overcoming learning challenges
            """,
            ExperienceLevel.MID: """
            - Answers should demonstrate practical experience and independent work
            - Include examples of successful project delivery and collaboration
            - Show progression in technical skills and responsibilities
            - Demonstrate ability to mentor junior team members
            - Include examples of process improvements and efficiency gains
            """,
            ExperienceLevel.SENIOR: """
            - Answers should show technical leadership and architectural thinking
            - Include examples of complex problem-solving and system design
            - Demonstrate ability to influence technical decisions across teams
            - Show experience mentoring and developing other engineers
            - Include examples of driving technical excellence and best practices
            """,
            ExperienceLevel.LEAD: """
            - Answers should emphasize people leadership and team building
            - Include examples of scaling teams and managing performance
            - Demonstrate ability to balance technical and business priorities
            - Show experience with cross-functional collaboration and stakeholder management
            - Include examples of organizational change and process improvement
            """,
            ExperienceLevel.PRINCIPAL: """
            - Answers should show strategic technical vision and industry expertise
            - Include examples of driving technical strategy across multiple teams
            - Demonstrate thought leadership and external influence
            - Show ability to identify and solve complex organizational challenges
            - Include examples of innovation and long-term technical planning
            """
        }
        return context_map.get(level, "General experience-appropriate context")
    
    def _get_round_context(self, round_number: InterviewRound) -> str:
        """Get context for answer generation based on interview round."""
        context_map = {
            InterviewRound.SCREENING: """
            - Answers should be concise and highlight key qualifications
            - Focus on motivation, cultural fit, and basic competency demonstration
            - Show enthusiasm for the role and company
            - Provide clear examples of relevant experience
            """,
            InterviewRound.TECHNICAL: """
            - Answers should demonstrate deep technical knowledge and problem-solving
            - Include specific technical details and implementation approaches
            - Show understanding of trade-offs and alternative solutions
            - Demonstrate hands-on experience with relevant technologies
            """,
            InterviewRound.BEHAVIORAL: """
            - Answers should use STAR method with specific, measurable outcomes
            - Focus on leadership, teamwork, and conflict resolution examples
            - Show personal growth and learning from challenges
            - Demonstrate emotional intelligence and interpersonal skills
            """,
            InterviewRound.FINAL: """
            - Answers should show strategic thinking and long-term vision
            - Include examples of organizational impact and influence
            - Demonstrate cultural alignment and leadership potential
            - Show understanding of business context and market dynamics
            """
        }
        return context_map.get(round_number, "General interview context")
