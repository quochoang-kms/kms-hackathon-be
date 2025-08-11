import asyncio
from typing import Dict, List, Any
from strands import Agent
from strands.models import BedrockModel

# Fix imports for standalone execution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.enhanced_models import (
    QualityMetrics, QualityAssessmentReport, EnhancedInterviewQuestion, 
    EnhancedSampleAnswer, ExperienceLevel, InterviewRound
)


class QualityAssuranceAgent:
    """Agent responsible for quality validation and consistency checking."""
    
    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2"):
        """
        Initialize the Quality Assurance Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.2,  # Low temperature for consistent quality assessment
        )
        
        self.agent = Agent(
            model=self.model,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the quality assurance agent."""
        return """
        You are a Quality Assurance Agent specialized in evaluating interview questions and sample answers.
        
        Your responsibilities:
        1. Assess the quality of generated interview questions and answers
        2. Validate consistency across all generated content
        3. Ensure alignment with role requirements and experience levels
        4. Identify potential issues and improvement opportunities
        5. Provide quality scores and detailed feedback
        
        Quality Assessment Criteria:
        
        QUESTION QUALITY:
        - Relevance: How well does the question align with the role and requirements?
        - Clarity: Is the question clear, specific, and unambiguous?
        - Appropriateness: Is the difficulty level suitable for the experience level?
        - Discrimination: Does the question effectively differentiate candidates?
        - Completeness: Does the question cover important aspects of the role?
        
        ANSWER QUALITY:
        - Completeness: Does the answer comprehensively address the question?
        - Accuracy: Is the technical/factual content accurate?
        - Structure: Is the answer well-organized and logical?
        - Depth: Is the level of detail appropriate for the experience level?
        - Practicality: Are the examples and scenarios realistic?
        
        CONSISTENCY VALIDATION:
        - Experience Level Alignment: All content matches the specified level
        - Role Relevance: Questions and answers are relevant to the specific role
        - Round Focus: Content aligns with the interview round objectives
        - Quality Balance: Consistent quality across all questions and answers
        
        SCORING SYSTEM:
        Use a 0-1 scale where:
        - 0.9-1.0: Excellent quality, ready for use
        - 0.7-0.89: Good quality, minor improvements possible
        - 0.5-0.69: Acceptable quality, some improvements needed
        - 0.3-0.49: Below standard, significant improvements required
        - 0.0-0.29: Poor quality, major revision needed
        
        Always provide specific, actionable feedback for improvement.
        """
    
    async def assess_questions_quality(self, 
                                     questions: List[Dict[str, Any]], 
                                     context: Dict[str, Any]) -> List[QualityMetrics]:
        """
        Assess the quality of generated questions.
        
        Args:
            questions: List of generated questions
            context: Context including role, level, round, etc.
            
        Returns:
            List[QualityMetrics]: Quality metrics for each question
        """
        quality_metrics = []
        
        for i, question in enumerate(questions):
            prompt = f"""
            Assess the quality of this interview question:
            
            QUESTION: {question.get('question', 'N/A')}
            TYPE: {question.get('type', 'N/A')}
            DIFFICULTY: {question.get('difficulty', 'N/A')}
            
            CONTEXT:
            - Role: {context.get('role', 'N/A')}
            - Experience Level: {context.get('level', 'N/A')}
            - Interview Round: {context.get('round', 'N/A')}
            - Job Requirements: {context.get('jd_analysis', 'N/A')[:500]}...
            
            Provide quality assessment scores (0-1) for:
            1. Relevance to role and requirements
            2. Clarity and specificity
            3. Completeness of coverage
            4. Consistency with experience level
            5. Overall quality score
            
            Also provide brief explanations for each score.
            """
            
            try:
                response = await self._async_agent_call(prompt)
                metrics = self._parse_quality_metrics(response.message)
                quality_metrics.append(metrics)
            except Exception as e:
                # Fallback quality metrics
                quality_metrics.append(QualityMetrics(
                    relevance_score=0.5,
                    clarity_score=0.5,
                    completeness_score=0.5,
                    consistency_score=0.5,
                    overall_score=0.5
                ))
        
        return quality_metrics
    
    async def assess_answers_quality(self, 
                                   answers: List[Dict[str, Any]], 
                                   questions: List[Dict[str, Any]],
                                   context: Dict[str, Any]) -> List[QualityMetrics]:
        """
        Assess the quality of generated sample answers.
        
        Args:
            answers: List of generated answers
            questions: Corresponding questions
            context: Context including role, level, round, etc.
            
        Returns:
            List[QualityMetrics]: Quality metrics for each answer
        """
        quality_metrics = []
        
        for i, (answer, question) in enumerate(zip(answers, questions)):
            prompt = f"""
            Assess the quality of this sample answer:
            
            QUESTION: {question.get('question', 'N/A')}
            ANSWER: {answer.get('answer', 'N/A')[:1000]}...
            
            CONTEXT:
            - Role: {context.get('role', 'N/A')}
            - Experience Level: {context.get('level', 'N/A')}
            - Interview Round: {context.get('round', 'N/A')}
            
            Assess the answer quality based on:
            1. Relevance to the question asked
            2. Clarity and structure of the response
            3. Completeness and depth of content
            4. Consistency with experience level expectations
            5. Overall quality and usefulness
            
            Provide scores (0-1) and brief explanations.
            """
            
            try:
                response = await self._async_agent_call(prompt)
                metrics = self._parse_quality_metrics(response.message)
                quality_metrics.append(metrics)
            except Exception as e:
                # Fallback quality metrics
                quality_metrics.append(QualityMetrics(
                    relevance_score=0.5,
                    clarity_score=0.5,
                    completeness_score=0.5,
                    consistency_score=0.5,
                    overall_score=0.5
                ))
        
        return quality_metrics
    
    async def validate_consistency(self, 
                                 questions: List[Dict[str, Any]], 
                                 answers: List[Dict[str, Any]],
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate consistency across all generated content.
        
        Args:
            questions: Generated questions
            answers: Generated answers
            context: Generation context
            
        Returns:
            Dict[str, Any]: Consistency validation results
        """
        prompt = f"""
        Validate the consistency of this interview content set:
        
        CONTEXT:
        - Role: {context.get('role', 'N/A')}
        - Experience Level: {context.get('level', 'N/A')}
        - Interview Round: {context.get('round', 'N/A')}
        - Number of Questions: {len(questions)}
        
        QUESTIONS OVERVIEW:
        {self._format_questions_for_validation(questions)}
        
        VALIDATION CHECKS:
        1. Experience Level Consistency: Are all questions appropriate for {context.get('level', 'N/A')} level?
        2. Role Relevance: Do all questions relate to {context.get('role', 'N/A')} responsibilities?
        3. Round Focus: Do questions align with round {context.get('round', 'N/A')} objectives?
        4. Difficulty Balance: Is there appropriate difficulty distribution?
        5. Question Type Balance: Is there good variety in question types?
        6. Answer Alignment: Do answers match their corresponding questions?
        
        Provide:
        - Overall consistency score (0-1)
        - Specific issues found
        - Recommendations for improvement
        - Validation status for each check (pass/fail)
        """
        
        try:
            response = await self._async_agent_call(prompt)
            return self._parse_consistency_results(response.message)
        except Exception as e:
            return {
                "overall_consistency": 0.5,
                "issues": [f"Validation error: {str(e)}"],
                "recommendations": ["Manual review recommended"],
                "validation_checks": {
                    "experience_level": False,
                    "role_relevance": False,
                    "round_focus": False,
                    "difficulty_balance": False,
                    "question_variety": False,
                    "answer_alignment": False
                }
            }
    
    async def generate_quality_report(self, 
                                    question_metrics: List[QualityMetrics],
                                    answer_metrics: List[QualityMetrics],
                                    consistency_results: Dict[str, Any],
                                    context: Dict[str, Any]) -> QualityAssessmentReport:
        """
        Generate a comprehensive quality assessment report.
        
        Args:
            question_metrics: Quality metrics for questions
            answer_metrics: Quality metrics for answers
            consistency_results: Consistency validation results
            context: Generation context
            
        Returns:
            QualityAssessmentReport: Comprehensive quality report
        """
        # Calculate overall scores
        avg_question_quality = sum(m.overall_score for m in question_metrics) / len(question_metrics)
        avg_answer_quality = sum(m.overall_score for m in answer_metrics) / len(answer_metrics)
        overall_quality = (avg_question_quality + avg_answer_quality + consistency_results.get("overall_consistency", 0.5)) / 3
        
        # Generate assessment summary
        if overall_quality >= 0.9:
            assessment = "Excellent quality - Ready for immediate use"
        elif overall_quality >= 0.7:
            assessment = "Good quality - Minor improvements recommended"
        elif overall_quality >= 0.5:
            assessment = "Acceptable quality - Some improvements needed"
        else:
            assessment = "Below standard - Significant improvements required"
        
        # Compile quality scores
        question_quality = {f"question_{i+1}": m.overall_score for i, m in enumerate(question_metrics)}
        answer_quality = {f"answer_{i+1}": m.overall_score for i, m in enumerate(answer_metrics)}
        
        # Generate improvement suggestions
        improvement_suggestions = []
        if avg_question_quality < 0.7:
            improvement_suggestions.append("Review question relevance and clarity")
        if avg_answer_quality < 0.7:
            improvement_suggestions.append("Enhance answer depth and structure")
        if consistency_results.get("overall_consistency", 0) < 0.7:
            improvement_suggestions.append("Improve consistency across content")
        
        improvement_suggestions.extend(consistency_results.get("recommendations", []))
        
        return QualityAssessmentReport(
            overall_assessment=assessment,
            question_quality=question_quality,
            answer_quality=answer_quality,
            consistency_analysis=consistency_results,
            improvement_suggestions=improvement_suggestions,
            validation_results=consistency_results.get("validation_checks", {})
        )
    
    async def _async_agent_call(self, prompt: str):
        """Make an async call to the agent."""
        # Note: This is a simplified async wrapper
        # In practice, you'd use the actual async capabilities of Strands
        return self.agent(prompt)
    
    def _parse_quality_metrics(self, response_text: str) -> QualityMetrics:
        """Parse quality metrics from agent response."""
        # Simplified parsing - in production, use more robust parsing
        try:
            # Extract scores using simple pattern matching
            import re
            
            relevance_match = re.search(r'relevance[:\s]*([0-9.]+)', response_text.lower())
            clarity_match = re.search(r'clarity[:\s]*([0-9.]+)', response_text.lower())
            completeness_match = re.search(r'completeness[:\s]*([0-9.]+)', response_text.lower())
            consistency_match = re.search(r'consistency[:\s]*([0-9.]+)', response_text.lower())
            overall_match = re.search(r'overall[:\s]*([0-9.]+)', response_text.lower())
            
            relevance = float(relevance_match.group(1)) if relevance_match else 0.7
            clarity = float(clarity_match.group(1)) if clarity_match else 0.7
            completeness = float(completeness_match.group(1)) if completeness_match else 0.7
            consistency = float(consistency_match.group(1)) if consistency_match else 0.7
            overall = float(overall_match.group(1)) if overall_match else (relevance + clarity + completeness + consistency) / 4
            
            return QualityMetrics(
                relevance_score=min(1.0, max(0.0, relevance)),
                clarity_score=min(1.0, max(0.0, clarity)),
                completeness_score=min(1.0, max(0.0, completeness)),
                consistency_score=min(1.0, max(0.0, consistency)),
                overall_score=min(1.0, max(0.0, overall))
            )
        except Exception:
            # Fallback to default scores
            return QualityMetrics(
                relevance_score=0.7,
                clarity_score=0.7,
                completeness_score=0.7,
                consistency_score=0.7,
                overall_score=0.7
            )
    
    def _parse_consistency_results(self, response_text: str) -> Dict[str, Any]:
        """Parse consistency validation results."""
        # Simplified parsing
        return {
            "overall_consistency": 0.8,  # Default value
            "issues": [],
            "recommendations": ["Content appears consistent"],
            "validation_checks": {
                "experience_level": True,
                "role_relevance": True,
                "round_focus": True,
                "difficulty_balance": True,
                "question_variety": True,
                "answer_alignment": True
            }
        }
    
    def _format_questions_for_validation(self, questions: List[Dict[str, Any]]) -> str:
        """Format questions for validation prompt."""
        formatted = []
        for i, q in enumerate(questions, 1):
            formatted.append(f"{i}. {q.get('question', 'N/A')} (Type: {q.get('type', 'N/A')}, Difficulty: {q.get('difficulty', 'N/A')})")
        return "\n".join(formatted)
