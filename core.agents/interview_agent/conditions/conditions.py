
def is_matched_skill(state):
    """ Check if the matching score >= 80% is matched."""

    matched_skill = state.results.get("SKILL_MATCHER")
    if not matched_skill:
        return False
    result_text = str(matched_skill.result)
    return "successful" in result_text.lower()
  
def is_analyzer_done(state):
    """ Check if the JD and CV analyzers are done."""
    
    jd_result = state.results.get("JD_ANALYZER")
    cv_result = state.results.get("CV_ANALYZER")
    
    return jd_result is not None and cv_result is not None

def is_skill_matching_done(state):
    """ Check if the skill matching is completed."""
    
    skill_matcher_result = state.results.get("SKILL_MATCHER")
    
    return skill_matcher_result is not None 