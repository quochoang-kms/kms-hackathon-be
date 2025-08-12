"""Main Interview Preparation System using Agent Graph"""

from typing import Dict, List, Any, Union
from strands_agents import Agent, agent_graph, journal
from .document_parser import DocumentParserAgent
from .jd_analyzer import JDAnalyzerAgent
from .cv_analyzer import CVAnalyzerAgent
from .skills_matcher import SkillsMatcherAgent
from .question_generator import QuestionGeneratorAgent
from .answer_evaluator import AnswerEvaluatorAgent
import logging
import os

logger = logging.getLogger(__name__)

class InterviewPreparationSystem(Agent):
    """Main orchestrator for the interview preparation system"""
    
    def __init__(self, model_id: str = None, region: str = None, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize model configuration
        self.model_id = model_id or os.getenv('MODEL_ID', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0')
        self.region = region or os.getenv('REGION', 'us-west-2')
        
        # Initialize agents
        self.document_parser = DocumentParserAgent(model_id=self.model_id, region=self.region)
        self.jd_analyzer = JDAnalyzerAgent(model_id=self.model_id, region=self.region)
        self.cv_analyzer = CVAnalyzerAgent(model_id=self.model_id, region=self.region)
        self.skills_matcher = SkillsMatcherAgent(model_id=self.model_id, region=self.region)
        self.question_generator = QuestionGeneratorAgent(model_id=self.model_id, region=self.region)
        self.answer_evaluator = AnswerEvaluatorAgent(model_id=self.model_id, region=self.region)
        
        # Validation constants
        self.valid_levels = ["Junior", "Mid", "Senior", "Lead", "Principal"]
        self.valid_rounds = [1, 2, 3, 4]
        self.valid_personas = ["Friendly", "Serious", "Analytical", "Collaborative", "Challenging"]
    
    @agent_graph
    async def prepare_interview(
        self,
        jd: Union[str, bytes],
        cv: Union[str, bytes],
        role: str,
        level: str = "Mid",
        round_number: int = 1,
        interview_persona: str = "Friendly"
    ) -> Dict[str, Any]:
        """Main workflow for interview preparation
        
        Args:
            jd: Job description (text, file path, or binary)
            cv: CV content (text, file path, or binary)
            role: Target role
            level: Experience level
            round_number: Interview round (1-4)
            interview_persona: Interview persona
            
        Returns:
            Complete interview preparation results
        """
        try:
            # Validate inputs
            self._validate_inputs(level, round_number, interview_persona)
            
            # Store initial context
            await journal.store("context", {
                "role": role,
                "level": level,
                "round_number": round_number,
                "interview_persona": interview_persona
            })
            
            # Step 1: Parse documents
            logger.info("Parsing JD and CV documents...")
            jd_parsed = await self.document_parser.parse_document(jd)
            cv_parsed = await self.document_parser.parse_document(cv)
            
            await journal.store("parsed_documents", {
                "jd": jd_parsed,
                "cv": cv_parsed
            })
            
            # Step 2: Analyze JD
            logger.info("Analyzing job description...")
            jd_analysis = await self.jd_analyzer.analyze_job_description(
                jd_parsed.get("text", ""),
                role,
                level
            )
            
            await journal.store("jd_analysis", jd_analysis)
            
            # Step 3: Analyze CV
            logger.info("Analyzing CV...")
            cv_analysis = await self.cv_analyzer.analyze_cv(
                cv_parsed.get("text", ""),
                role,
                level
            )
            
            await journal.store("cv_analysis", cv_analysis)
            
            # Step 4: Match skills
            logger.info("Matching skills...")
            skills_match = await self.skills_matcher.match_skills(jd_analysis, cv_analysis)
            
            await journal.store("skills_match", skills_match)
            
            # Step 5: Generate questions
            logger.info("Generating interview questions...")
            questions = await self.question_generator.generate_questions(
                skills_match,
                level,
                round_number,
                interview_persona,
                role
            )
            
            await journal.store("questions", questions)
            
            # Step 6: Generate evaluation criteria
            logger.info("Generating evaluation criteria...")
            evaluation_criteria = await self.answer_evaluator.generate_evaluation_criteria(
                questions.get("questions", []),
                level,
                interview_persona,
                skills_match
            )
            
            await journal.store("evaluation_criteria", evaluation_criteria)
            
            # Compile final results
            results = {
                "metadata": {
                    "role": role,
                    "level": level,
                    "round_number": round_number,
                    "round_name": {1: "Screening", 2: "Technical", 3: "Behavioral", 4: "Final"}.get(round_number),
                    "interview_persona": interview_persona,
                    "timestamp": self._get_timestamp()
                },
                "analysis_results": {
                    "jd_analysis": {
                        "required_skills": jd_analysis.get("required_skills", []),
                        "preferred_skills": jd_analysis.get("preferred_skills", []),
                        "soft_skills": jd_analysis.get("soft_skills", []),
                        "level_competencies": jd_analysis.get("level_competencies", [])
                    },
                    "cv_analysis": {
                        "technical_skills": cv_analysis.get("technical_skills", []),
                        "years_of_experience": cv_analysis.get("years_of_experience", 0),
                        "leadership_experience": cv_analysis.get("leadership_experience", []),
                        "level_alignment": cv_analysis.get("level_alignment", "")
                    },
                    "skills_matching": {
                        "matched_skills": skills_match.get("matched_skills", []),
                        "missing_skills": skills_match.get("missing_skills", []),
                        "strong_areas": skills_match.get("strong_areas", []),
                        "red_flags": skills_match.get("red_flags", []),
                        "overall_match_score": skills_match.get("overall_match_score", 0)
                    }
                },
                "interview_preparation": {
                    "questions": questions.get("questions", []),
                    "total_questions": questions.get("total_questions", 0),
                    "evaluation_criteria": evaluation_criteria.get("evaluations", [])
                },
                "status": "completed"
            }
            
            logger.info("Interview preparation completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Interview preparation failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "metadata": {
                    "role": role,
                    "level": level,
                    "round_number": round_number,
                    "interview_persona": interview_persona
                }
            }
    
    def _validate_inputs(self, level: str, round_number: int, interview_persona: str):
        """Validate input parameters"""
        if level not in self.valid_levels:
            raise ValueError(f"Invalid level: {level}. Must be one of {self.valid_levels}")
        
        if round_number not in self.valid_rounds:
            raise ValueError(f"Invalid round number: {round_number}. Must be one of {self.valid_rounds}")
        
        if interview_persona not in self.valid_personas:
            raise ValueError(f"Invalid persona: {interview_persona}. Must be one of {self.valid_personas}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of the analysis from journal"""
        try:
            context = await journal.retrieve("context")
            skills_match = await journal.retrieve("skills_match")
            questions = await journal.retrieve("questions")
            
            return {
                "context": context,
                "match_score": skills_match.get("overall_match_score", 0),
                "question_count": questions.get("total_questions", 0),
                "strong_areas": skills_match.get("strong_areas", []),
                "areas_for_improvement": skills_match.get("missing_skills", [])
            }
        except Exception as e:
            logger.error(f"Failed to get analysis summary: {str(e)}")
            return {"error": str(e)}