
from utils.logger import logger


def is_matched_skill(state):
    """
    Check if skill matching score meets threshold (>=80).
    
    Args:
        state: Workflow state containing SKILL_MATCHER results
        
    Returns:
        bool: True if overall_match_score >= 80, False otherwise
    """
    import json
    import re
    
    matched_skill = state.results.get("SKILL_MATCHER")
    if not matched_skill:
        return False
    
    try:
        # Get the result text from SKILL_MATCHER
        result_text = matched_skill.result.message["content"][0]["text"]
        
        # Extract JSON from response (handles both markdown-wrapped and plain JSON)
        markdown_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
        if markdown_match:
            json_str = markdown_match.group(1).strip()
        else:
            json_match = re.search(r'(\{.*\})', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                return False
        
        # Parse JSON and check overall_match_score
        result_json = json.loads(json_str)
        overall_match_score = result_json.get("overall_match_score", 0)
        
        logger.info(f"Validating overall match score: {overall_match_score}")
        # Return True if score >= 80
        return overall_match_score >= 80
        
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError) as e:
        print(f"Error parsing SKILL_MATCHER result: {e}")
        return False
  
def is_analyzer_done(state):
    """
    Check if both JD and CV analysis are completed.
    
    Args:
        state: Workflow state containing analyzer results
        
    Returns:
        bool: True if both JD_ANALYZER and CV_ANALYZER are done
    """
    
    jd_result = state.results.get("JD_ANALYZER")
    cv_result = state.results.get("CV_ANALYZER")
    
    return jd_result is not None and cv_result is not None

def is_skill_matching_done(state):
    """
    Check if skill matching process is completed.
    
    Args:
        state: Workflow state containing SKILL_MATCHER results
        
    Returns:
        bool: True if SKILL_MATCHER result exists
    """
    
    skill_matcher_result = state.results.get("SKILL_MATCHER")
    
    return skill_matcher_result is not None 