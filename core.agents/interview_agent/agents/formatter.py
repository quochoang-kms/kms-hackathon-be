import asyncio
from typing import Dict, List, Any
from strands import Agent
from strands.models import BedrockModel

# Fix imports for standalone execution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.enhanced_models import (
    EnhancedInterviewResponse, EnhancedInterviewQuestion, EnhancedSampleAnswer,
    QualityMetrics, QualityAssessmentReport, AgentPerformanceMetrics,
    InterviewerGuidance, ExperienceLevel, InterviewRound
)


class FormatterAgent:
    """Agent responsible for formatting final output and creating comprehensive interview packages."""
    
    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2"):
        """
        Initialize the Formatter Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.2,  # Low temperature for consistent formatting
        )
        
        self.agent = Agent(
            model=self.model,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the formatter agent."""
        return """
        You are a Formatter Agent specialized in creating comprehensive, well-structured interview packages.
        
        Your responsibilities:
        1. Format generated questions and answers into a professional interview package
        2. Create comprehensive interviewer guidance and evaluation frameworks
        3. Generate structured interview flows and timing recommendations
        4. Provide detailed assessment rubrics and evaluation criteria
        5. Ensure all content is presentation-ready and actionable
        
        Formatting Guidelines:
        
        INTERVIEW QUESTIONS:
        - Clear, professional formatting
        - Logical ordering by importance and flow
        - Appropriate metadata (type, difficulty, timing)
        - Follow-up question suggestions
        - Evaluation criteria for each question
        
        SAMPLE ANSWERS:
        - Well-structured with clear frameworks (STAR, technical approach)
        - Key points highlighted for easy reference
        - Evaluation criteria and scoring guidance
        - Red flags and excellent indicators
        - Appropriate depth for experience level
        
        INTERVIEWER GUIDANCE:
        - Pre-interview preparation checklist
        - Interview flow and timing recommendations
        - Question transition strategies
        - Evaluation rubrics and scoring methods
        - Common pitfalls and best practices
        
        ASSESSMENT FRAMEWORK:
        - Comprehensive evaluation criteria
        - Scoring rubrics for different question types
        - Candidate assessment guidelines
        - Decision-making frameworks
        - Documentation templates
        
        Always ensure content is:
        - Professional and polished
        - Actionable and practical
        - Comprehensive yet concise
        - Suitable for various interviewer experience levels
        - Compliant with best practices and legal considerations
        """
    
    async def create_final_output(self,
                                questions_data: Dict[str, Any],
                                answers_data: Dict[str, Any],
                                quality_data: Dict[str, Any],
                                performance_metrics: List[AgentPerformanceMetrics],
                                context: Dict[str, Any]) -> EnhancedInterviewResponse:
        """
        Create the final formatted interview response.
        
        Args:
            questions_data: Generated questions with metadata
            answers_data: Generated answers with metadata
            quality_data: Quality assessment results
            performance_metrics: Agent performance metrics
            context: Generation context
            
        Returns:
            EnhancedInterviewResponse: Comprehensive formatted response
        """
        # Format questions
        formatted_questions = await self._format_questions(questions_data, context)
        
        # Format answers
        formatted_answers = await self._format_answers(answers_data, context)
        
        # Generate interviewer guidance
        interviewer_guidance = await self._generate_interviewer_guidance(
            formatted_questions, formatted_answers, context
        )
        
        # Create evaluation framework
        evaluation_framework = await self._create_evaluation_framework(
            formatted_questions, formatted_answers, context
        )
        
        # Calculate overall quality score
        overall_quality = self._calculate_overall_quality(quality_data)
        
        # Generate metadata
        generation_metadata = self._create_generation_metadata(context, performance_metrics)
        
        return EnhancedInterviewResponse(
            questions=formatted_questions,
            sample_answers=formatted_answers,
            interview_focus=self._generate_interview_focus(context),
            preparation_tips=interviewer_guidance.get('preparation_tips', []),
            overall_quality_score=overall_quality,
            processing_metrics=performance_metrics,
            quality_report=quality_data,
            generation_metadata=generation_metadata,
            interview_structure=interviewer_guidance.get('interview_structure', {}),
            evaluation_framework=evaluation_framework,
            candidate_assessment_guide=interviewer_guidance.get('assessment_guide', [])
        )
    
    async def _format_questions(self, questions_data: Dict[str, Any], context: Dict[str, Any]) -> List[EnhancedInterviewQuestion]:
        """Format questions with enhanced metadata."""
        questions = questions_data.get('questions', [])
        quality_metrics = questions_data.get('quality_metrics', [])
        
        formatted_questions = []
        
        for i, (question_data, quality) in enumerate(zip(questions, quality_metrics)):
            # Generate follow-up questions
            follow_ups = await self._generate_follow_up_questions(question_data, context)
            
            # Generate tags
            tags = self._generate_question_tags(question_data, context)
            
            formatted_question = EnhancedInterviewQuestion(
                question=question_data.get('question', ''),
                type=question_data.get('type', 'technical'),
                difficulty=question_data.get('difficulty', 'intermediate'),
                expected_duration=question_data.get('expected_duration', 5),
                quality_metrics=quality,
                tags=tags,
                follow_up_questions=follow_ups
            )
            
            formatted_questions.append(formatted_question)
        
        return formatted_questions
    
    async def _format_answers(self, answers_data: Dict[str, Any], context: Dict[str, Any]) -> List[EnhancedSampleAnswer]:
        """Format answers with enhanced metadata."""
        answers = answers_data.get('answers', [])
        quality_metrics = answers_data.get('quality_metrics', [])
        
        formatted_answers = []
        
        for i, (answer_data, quality) in enumerate(zip(answers, quality_metrics)):
            # Determine answer framework
            framework = self._determine_answer_framework(answer_data)
            
            # Generate red flags and excellent indicators
            red_flags = self._generate_red_flags(answer_data, context)
            excellent_indicators = self._generate_excellent_indicators(answer_data, context)
            
            formatted_answer = EnhancedSampleAnswer(
                question=answer_data.get('question', ''),
                answer=answer_data.get('answer', ''),
                key_points=answer_data.get('key_points', []),
                evaluation_criteria=answer_data.get('evaluation_criteria', []),
                quality_metrics=quality,
                answer_framework=framework,
                red_flags=red_flags,
                excellent_indicators=excellent_indicators
            )
            
            formatted_answers.append(formatted_answer)
        
        return formatted_answers
    
    async def _generate_interviewer_guidance(self, 
                                           questions: List[EnhancedInterviewQuestion],
                                           answers: List[EnhancedSampleAnswer],
                                           context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive interviewer guidance."""
        prompt = f"""
        Create comprehensive interviewer guidance for this interview:
        
        CONTEXT:
        - Role: {context.get('role', 'N/A')}
        - Experience Level: {context.get('level', 'N/A')}
        - Interview Round: {context.get('round', 'N/A')}
        - Number of Questions: {len(questions)}
        
        QUESTIONS OVERVIEW:
        {self._format_questions_overview(questions)}
        
        Generate guidance for:
        1. Pre-interview preparation steps
        2. Interview structure and flow
        3. Question timing and transitions
        4. Candidate assessment guidelines
        5. Common pitfalls to avoid
        6. Best practices for this specific interview
        
        Format as actionable, practical guidance for interviewers.
        """
        
        try:
            response = await self._async_agent_call(prompt)
            return self._parse_interviewer_guidance(response.message)
        except Exception as e:
            return self._get_default_interviewer_guidance(context)
    
    async def _create_evaluation_framework(self,
                                         questions: List[EnhancedInterviewQuestion],
                                         answers: List[EnhancedSampleAnswer],
                                         context: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive evaluation framework."""
        prompt = f"""
        Create a comprehensive evaluation framework for this interview:
        
        CONTEXT:
        - Role: {context.get('role', 'N/A')}
        - Experience Level: {context.get('level', 'N/A')}
        - Interview Round: {context.get('round', 'N/A')}
        
        Create evaluation framework including:
        1. Scoring rubrics for each question type
        2. Overall candidate assessment criteria
        3. Decision-making guidelines
        4. Comparison framework for multiple candidates
        5. Documentation templates
        6. Legal and bias considerations
        
        Ensure framework is practical and actionable.
        """
        
        try:
            response = await self._async_agent_call(prompt)
            return self._parse_evaluation_framework(response.message)
        except Exception as e:
            return self._get_default_evaluation_framework(context)
    
    async def _generate_follow_up_questions(self, question_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate follow-up questions for a given question."""
        question_text = question_data.get('question', '')
        question_type = question_data.get('type', 'technical')
        
        # Generate 2-3 follow-up questions based on the main question
        follow_ups = []
        
        if question_type == 'behavioral':
            follow_ups = [
                "What would you do differently if you faced a similar situation again?",
                "How did this experience change your approach to similar challenges?",
                "What did you learn from this experience?"
            ]
        elif question_type == 'technical':
            follow_ups = [
                "How would you optimize this solution for better performance?",
                "What are the potential drawbacks of this approach?",
                "How would you handle edge cases in this scenario?"
            ]
        elif question_type == 'situational':
            follow_ups = [
                "What factors would influence your decision-making process?",
                "How would you communicate this decision to stakeholders?",
                "What metrics would you use to measure success?"
            ]
        else:  # cultural_fit
            follow_ups = [
                "Can you give me a specific example of this?",
                "How do you think this aligns with our company values?",
                "What motivates you most about this aspect?"
            ]
        
        return follow_ups[:2]  # Return top 2 follow-ups
    
    def _generate_question_tags(self, question_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate tags for question categorization."""
        tags = []
        
        # Add type-based tags
        question_type = question_data.get('type', 'technical')
        tags.append(question_type)
        
        # Add difficulty tag
        difficulty = question_data.get('difficulty', 'intermediate')
        tags.append(difficulty)
        
        # Add role-based tags
        role = context.get('role', '').lower()
        if 'engineer' in role:
            tags.append('engineering')
        elif 'manager' in role:
            tags.append('management')
        elif 'data' in role:
            tags.append('data')
        elif 'product' in role:
            tags.append('product')
        
        # Add level-based tags
        level = context.get('level', '')
        if level:
            tags.append(level.lower())
        
        return tags
    
    def _determine_answer_framework(self, answer_data: Dict[str, Any]) -> str:
        """Determine the framework used in the answer."""
        answer_text = answer_data.get('answer', '').lower()
        
        if any(word in answer_text for word in ['situation', 'task', 'action', 'result']):
            return 'STAR'
        elif any(word in answer_text for word in ['algorithm', 'complexity', 'implementation']):
            return 'Technical'
        elif any(word in answer_text for word in ['problem', 'solution', 'approach']):
            return 'Problem-Solving'
        else:
            return 'Structured'
    
    def _generate_red_flags(self, answer_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate red flags for candidate responses."""
        return [
            "Vague or non-specific examples",
            "Inability to explain technical details",
            "Blaming others without taking responsibility",
            "Lack of measurable outcomes or results",
            "Inconsistent or contradictory information"
        ]
    
    def _generate_excellent_indicators(self, answer_data: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate excellent indicators for candidate responses."""
        return [
            "Specific, detailed examples with context",
            "Clear demonstration of problem-solving skills",
            "Quantifiable results and impact",
            "Shows learning and growth mindset",
            "Demonstrates leadership and initiative"
        ]
    
    def _calculate_overall_quality(self, quality_data: Dict[str, Any]) -> float:
        """Calculate overall quality score."""
        if not quality_data:
            return 0.7  # Default score
        
        # Extract quality scores from different components
        question_scores = quality_data.get('question_quality', {}).values()
        answer_scores = quality_data.get('answer_quality', {}).values()
        consistency_score = quality_data.get('consistency_analysis', {}).get('overall_consistency', 0.7)
        
        # Calculate weighted average
        avg_question_quality = sum(question_scores) / len(question_scores) if question_scores else 0.7
        avg_answer_quality = sum(answer_scores) / len(answer_scores) if answer_scores else 0.7
        
        overall_quality = (avg_question_quality * 0.4 + avg_answer_quality * 0.4 + consistency_score * 0.2)
        
        return round(overall_quality, 2)
    
    def _create_generation_metadata(self, context: Dict[str, Any], performance_metrics: List[AgentPerformanceMetrics]) -> Dict[str, Any]:
        """Create generation metadata."""
        total_processing_time = sum(m.processing_time for m in performance_metrics)
        total_tokens = sum(m.token_usage for m in performance_metrics)
        
        return {
            "generation_timestamp": context.get('timestamp', ''),
            "total_processing_time": total_processing_time,
            "total_token_usage": total_tokens,
            "agents_used": [m.agent_name for m in performance_metrics],
            "parallel_processing_enabled": context.get('parallel_processing', False),
            "quality_assurance_enabled": context.get('quality_assurance', False)
        }
    
    def _generate_interview_focus(self, context: Dict[str, Any]) -> str:
        """Generate interview focus description."""
        role = context.get('role', 'N/A')
        level = context.get('level', 'N/A')
        round_num = context.get('round', 1)
        
        round_focus_map = {
            1: "Initial screening and basic qualification assessment",
            2: "Deep technical evaluation and problem-solving skills",
            3: "Behavioral assessment and cultural fit evaluation",
            4: "Final assessment and decision-making evaluation"
        }
        
        focus = round_focus_map.get(round_num, "General interview assessment")
        return f"{focus} for a {level} {role} position."
    
    async def _async_agent_call(self, prompt: str):
        """Make an async call to the agent."""
        return self.agent(prompt)
    
    def _format_questions_overview(self, questions: List[EnhancedInterviewQuestion]) -> str:
        """Format questions overview for prompts."""
        overview = []
        for i, q in enumerate(questions, 1):
            overview.append(f"{i}. {q.question} (Type: {q.type}, Difficulty: {q.difficulty})")
        return "\n".join(overview)
    
    def _parse_interviewer_guidance(self, response_text: str) -> Dict[str, Any]:
        """Parse interviewer guidance from response."""
        # Simplified parsing - in production, use more robust parsing
        return {
            "preparation_tips": [
                "Review candidate's background thoroughly",
                "Prepare follow-up questions based on their experience",
                "Set up a comfortable interview environment",
                "Have evaluation criteria ready"
            ],
            "interview_structure": {
                "introduction": "5 minutes - Welcome and role overview",
                "main_questions": "30-40 minutes - Core interview questions",
                "candidate_questions": "10 minutes - Candidate's questions",
                "wrap_up": "5 minutes - Next steps and closing"
            },
            "assessment_guide": [
                "Focus on specific examples and outcomes",
                "Assess both technical skills and cultural fit",
                "Take detailed notes for comparison",
                "Evaluate communication and problem-solving approach"
            ]
        }
    
    def _parse_evaluation_framework(self, response_text: str) -> Dict[str, Any]:
        """Parse evaluation framework from response."""
        return {
            "scoring_rubric": {
                "technical_skills": "1-5 scale based on depth and accuracy",
                "problem_solving": "1-5 scale based on approach and creativity",
                "communication": "1-5 scale based on clarity and engagement",
                "cultural_fit": "1-5 scale based on values alignment"
            },
            "decision_criteria": {
                "strong_hire": "4+ average across all areas",
                "hire": "3.5+ average with no major red flags",
                "no_hire": "Below 3.5 average or major concerns"
            },
            "documentation_template": {
                "strengths": "List candidate's key strengths",
                "concerns": "Note any areas of concern",
                "overall_assessment": "Summary recommendation",
                "next_steps": "Recommended next steps"
            }
        }
    
    def _get_default_interviewer_guidance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get default interviewer guidance."""
        return {
            "preparation_tips": [
                "Review job description and candidate resume",
                "Prepare follow-up questions",
                "Set up interview environment",
                "Have evaluation criteria ready"
            ],
            "interview_structure": {
                "introduction": "5 minutes",
                "main_questions": "35 minutes", 
                "candidate_questions": "10 minutes",
                "wrap_up": "5 minutes"
            },
            "assessment_guide": [
                "Focus on specific examples",
                "Assess technical and soft skills",
                "Take detailed notes",
                "Evaluate overall fit"
            ]
        }
    
    def _get_default_evaluation_framework(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get default evaluation framework."""
        return {
            "scoring_rubric": {
                "technical_skills": "1-5 scale",
                "problem_solving": "1-5 scale",
                "communication": "1-5 scale",
                "cultural_fit": "1-5 scale"
            },
            "decision_criteria": {
                "strong_hire": "4+ average",
                "hire": "3.5+ average",
                "no_hire": "Below 3.5 average"
            }
        }
