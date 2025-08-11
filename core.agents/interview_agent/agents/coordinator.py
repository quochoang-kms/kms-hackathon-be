from strands import Agent
from strands.models import BedrockModel
from strands_tools import agent_graph
from ..models import InterviewRequest, InterviewResponse, ExperienceLevel, InterviewRound
from .document_processor import DocumentProcessorAgent
from .question_generator import QuestionGeneratorAgent
from .answer_generator import AnswerGeneratorAgent
import json
import re


class CoordinatorAgent:
    """Main coordinator agent that orchestrates the multi-agent workflow."""
    
    def __init__(self, model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0", region: str = "us-west-2"):
        """
        Initialize the Coordinator Agent.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
        """
        self.model = BedrockModel(
            model_id=model_id,
            region_name=region,
            temperature=0.2,  # Low temperature for consistent coordination
        )
        
        # Initialize sub-agents
        self.document_processor = DocumentProcessorAgent(model_id, region)
        self.question_generator = QuestionGeneratorAgent(model_id, region)
        self.answer_generator = AnswerGeneratorAgent(model_id, region)
        
        self.agent = Agent(
            model=self.model,
            tools=[agent_graph],
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the coordinator agent."""
        return """
        You are the Coordinator Agent for an Interview Generation System. Your role is to orchestrate a multi-agent workflow to generate high-quality interview questions and sample answers.
        
        Your responsibilities:
        1. Coordinate the workflow between Document Processor, Question Generator, and Answer Generator agents
        2. Ensure data flows correctly between agents
        3. Validate outputs and ensure quality standards
        4. Format final results into a structured response
        5. Handle errors and provide fallback strategies
        
        Workflow Steps:
        1. Document Processing: Extract and analyze JD and CV content
        2. Question Generation: Create relevant interview questions based on analysis
        3. Answer Generation: Generate sample answers for the questions
        4. Quality Assurance: Validate and format final output
        
        Quality Standards:
        - Questions must be relevant to the role and experience level
        - Answers must be comprehensive and well-structured
        - Content must be appropriate for the interview round
        - Output must be properly formatted and complete
        
        Always ensure the workflow completes successfully and provides valuable interview preparation materials.
        """
    
    def generate_interview_content(self, request: InterviewRequest) -> InterviewResponse:
        """
        Generate interview questions and sample answers based on the request.
        
        Args:
            request: Interview generation request with all required parameters
            
        Returns:
            InterviewResponse: Generated questions and answers with metadata
        """
        try:
            # Step 1: Process documents
            print("Step 1: Processing documents...")
            document_analysis = self.document_processor.process_content_directly(
                request.jd_content, 
                request.cv_content
            )
            
            # Step 2: Generate questions
            print("Step 2: Generating interview questions...")
            questions_result = self.question_generator.generate_questions(
                document_analysis["analysis"],
                request.role,
                request.level,
                request.round_number,
                request.num_questions
            )
            
            # Step 3: Generate sample answers
            print("Step 3: Generating sample answers...")
            answers_result = self.answer_generator.generate_answers(
                questions_result["questions"],
                document_analysis["analysis"],
                request.role,
                request.level,
                request.round_number
            )
            
            # Step 4: Format and validate final response
            print("Step 4: Formatting final response...")
            final_response = self._format_final_response(
                questions_result,
                answers_result,
                request
            )
            
            return final_response
            
        except Exception as e:
            print(f"Error in workflow: {str(e)}")
            return self._create_error_response(str(e))
    
    def generate_from_files(self, 
                           jd_file_path: str,
                           cv_file_path: str,
                           role: str,
                           level: ExperienceLevel,
                           round_number: InterviewRound,
                           num_questions: int = 5) -> InterviewResponse:
        """
        Generate interview content from file paths.
        
        Args:
            jd_file_path: Path to job description file
            cv_file_path: Path to CV file
            role: Job role
            level: Experience level
            round_number: Interview round
            num_questions: Number of questions to generate
            
        Returns:
            InterviewResponse: Generated interview content
        """
        try:
            # Step 1: Process document files
            print("Step 1: Processing document files...")
            document_analysis = self.document_processor.process_documents(
                jd_file_path,
                cv_file_path
            )
            
            # Step 2: Generate questions
            print("Step 2: Generating interview questions...")
            questions_result = self.question_generator.generate_questions(
                document_analysis["analysis"],
                role,
                level,
                round_number,
                num_questions
            )
            
            # Step 3: Generate sample answers
            print("Step 3: Generating sample answers...")
            answers_result = self.answer_generator.generate_answers(
                questions_result["questions"],
                document_analysis["analysis"],
                role,
                level,
                round_number
            )
            
            # Step 4: Format final response
            print("Step 4: Formatting final response...")
            request = InterviewRequest(
                jd_content="",  # Not needed for formatting
                cv_content="",  # Not needed for formatting
                role=role,
                level=level,
                round_number=round_number,
                num_questions=num_questions
            )
            
            final_response = self._format_final_response(
                questions_result,
                answers_result,
                request
            )
            
            return final_response
            
        except Exception as e:
            print(f"Error in file-based workflow: {str(e)}")
            return self._create_error_response(str(e))
    
    def _format_final_response(self, 
                              questions_result: dict,
                              answers_result: dict,
                              request: InterviewRequest) -> InterviewResponse:
        """
        Format the final response from agent outputs.
        
        Args:
            questions_result: Output from question generator
            answers_result: Output from answer generator
            request: Original request
            
        Returns:
            InterviewResponse: Formatted final response
        """
        # Parse questions and answers from agent responses
        questions = self._parse_questions(questions_result["questions"])
        sample_answers = self._parse_answers(answers_result["sample_answers"])
        
        # Generate interview focus and preparation tips
        interview_focus = self._generate_interview_focus(request)
        preparation_tips = self._generate_preparation_tips(request)
        
        return InterviewResponse(
            questions=questions,
            sample_answers=sample_answers,
            interview_focus=interview_focus,
            preparation_tips=preparation_tips
        )
    
    def _parse_questions(self, questions_text: str) -> list:
        """Parse questions from agent response text."""
        # This is a simplified parser - in production, you might want more robust parsing
        questions = []
        
        # Try to extract structured question information
        question_blocks = re.split(r'\n\s*(?=\d+\.|\*|\-)', questions_text)
        
        for block in question_blocks:
            if len(block.strip()) > 10:  # Filter out very short blocks
                # Extract question text (first line or sentence)
                lines = block.strip().split('\n')
                question_text = lines[0].strip()
                
                # Clean up question text
                question_text = re.sub(r'^\d+\.\s*|\*\s*|\-\s*', '', question_text)
                
                if question_text:
                    # Try to determine question type and difficulty from context
                    question_type = self._determine_question_type(block)
                    difficulty = self._determine_difficulty(block)
                    duration = self._determine_duration(block)
                    
                    from ..models import InterviewQuestion
                    questions.append(InterviewQuestion(
                        question=question_text,
                        type=question_type,
                        difficulty=difficulty,
                        expected_duration=duration
                    ))
        
        return questions[:10]  # Limit to reasonable number
    
    def _parse_answers(self, answers_text: str) -> list:
        """Parse sample answers from agent response text."""
        answers = []
        
        # Split by question/answer pairs
        answer_blocks = re.split(r'\n\s*(?=Question|Answer|Q\d+|A\d+)', answers_text)
        
        current_question = ""
        current_answer = ""
        
        for block in answer_blocks:
            block = block.strip()
            if not block:
                continue
                
            if block.lower().startswith(('question', 'q')):
                if current_question and current_answer:
                    # Save previous pair
                    from ..models import SampleAnswer
                    answers.append(SampleAnswer(
                        question=current_question,
                        answer=current_answer,
                        key_points=self._extract_key_points(current_answer),
                        evaluation_criteria=self._extract_evaluation_criteria(current_answer)
                    ))
                current_question = block
                current_answer = ""
            elif block.lower().startswith(('answer', 'a')):
                current_answer = block
            else:
                if current_answer:
                    current_answer += "\n" + block
                elif current_question:
                    current_question += "\n" + block
        
        # Don't forget the last pair
        if current_question and current_answer:
            from ..models import SampleAnswer
            answers.append(SampleAnswer(
                question=current_question,
                answer=current_answer,
                key_points=self._extract_key_points(current_answer),
                evaluation_criteria=self._extract_evaluation_criteria(current_answer)
            ))
        
        return answers
    
    def _determine_question_type(self, question_block: str) -> str:
        """Determine question type from context."""
        block_lower = question_block.lower()
        
        if any(word in block_lower for word in ['technical', 'code', 'algorithm', 'system', 'design']):
            return "technical"
        elif any(word in block_lower for word in ['tell me about', 'describe a time', 'how did you']):
            return "behavioral"
        elif any(word in block_lower for word in ['what would you do', 'how would you handle', 'imagine']):
            return "situational"
        else:
            return "cultural_fit"
    
    def _determine_difficulty(self, question_block: str) -> str:
        """Determine question difficulty from context."""
        block_lower = question_block.lower()
        
        if any(word in block_lower for word in ['basic', 'fundamental', 'simple']):
            return "basic"
        elif any(word in block_lower for word in ['advanced', 'complex', 'expert']):
            return "advanced"
        else:
            return "intermediate"
    
    def _determine_duration(self, question_block: str) -> int:
        """Determine expected answer duration."""
        # Look for duration mentions in the block
        duration_match = re.search(r'(\d+)\s*minutes?', question_block.lower())
        if duration_match:
            return int(duration_match.group(1))
        
        # Default durations based on question type
        if 'technical' in question_block.lower():
            return 5
        elif 'behavioral' in question_block.lower():
            return 4
        else:
            return 3
    
    def _extract_key_points(self, answer_text: str) -> list:
        """Extract key points from answer text."""
        # Simple extraction - look for bullet points or numbered items
        key_points = []
        
        lines = answer_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*')) or re.match(r'^\d+\.', line):
                key_points.append(line)
        
        # If no bullet points found, extract first few sentences
        if not key_points:
            sentences = re.split(r'[.!?]+', answer_text)
            key_points = [s.strip() for s in sentences[:3] if len(s.strip()) > 10]
        
        return key_points[:5]  # Limit to 5 key points
    
    def _extract_evaluation_criteria(self, answer_text: str) -> list:
        """Extract evaluation criteria from answer context."""
        # Default evaluation criteria based on common interview standards
        return [
            "Clarity and structure of response",
            "Specific examples and details provided",
            "Demonstration of relevant skills/experience",
            "Problem-solving approach",
            "Communication effectiveness"
        ]
    
    def _generate_interview_focus(self, request: InterviewRequest) -> str:
        """Generate interview focus description."""
        round_focus = {
            InterviewRound.SCREENING: "Initial assessment of basic qualifications, cultural fit, and candidate motivation",
            InterviewRound.TECHNICAL: "Deep evaluation of technical skills, problem-solving abilities, and role-specific competencies",
            InterviewRound.BEHAVIORAL: "Assessment of past experiences, leadership potential, teamwork, and soft skills",
            InterviewRound.FINAL: "Final evaluation of strategic thinking, cultural alignment, and decision-making readiness"
        }
        
        return f"{round_focus.get(request.round_number, 'General interview assessment')} for a {request.level.value} {request.role} position."
    
    def _generate_preparation_tips(self, request: InterviewRequest) -> list:
        """Generate preparation tips for interviewers."""
        base_tips = [
            "Review candidate's background thoroughly before the interview",
            "Prepare follow-up questions based on candidate responses",
            "Take detailed notes for comparison with other candidates",
            "Focus on specific examples and measurable outcomes",
            "Assess both technical competency and cultural fit"
        ]
        
        level_specific_tips = {
            ExperienceLevel.JUNIOR: [
                "Focus on learning potential and foundational knowledge",
                "Assess problem-solving approach rather than just correct answers"
            ],
            ExperienceLevel.SENIOR: [
                "Evaluate leadership and mentoring capabilities",
                "Assess architectural thinking and system design skills"
            ],
            ExperienceLevel.LEAD: [
                "Focus on people management and team building experience",
                "Evaluate strategic thinking and cross-functional collaboration"
            ]
        }
        
        tips = base_tips + level_specific_tips.get(request.level, [])
        return tips
    
    def _create_error_response(self, error_message: str) -> InterviewResponse:
        """Create an error response when workflow fails."""
        from ..models import InterviewQuestion, SampleAnswer
        
        return InterviewResponse(
            questions=[InterviewQuestion(
                question=f"Error occurred during generation: {error_message}",
                type="technical",
                difficulty="basic",
                expected_duration=1
            )],
            sample_answers=[SampleAnswer(
                question="Error occurred",
                answer="Please check the input parameters and try again.",
                key_points=["Error in processing"],
                evaluation_criteria=["N/A"]
            )],
            interview_focus="Error in generation process",
            preparation_tips=["Please retry with valid inputs"]
        )
