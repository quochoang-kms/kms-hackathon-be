import re
from typing import Dict, List
from strands import tool


@tool
def analyze_jd_content(jd_content: str) -> Dict[str, any]:
    """
    Analyze job description content to extract key information.
    
    Args:
        jd_content: Job description text content
        
    Returns:
        Dict containing analyzed JD information
    """
    analysis = {
        "required_skills": _extract_skills(jd_content),
        "responsibilities": _extract_responsibilities(jd_content),
        "qualifications": _extract_qualifications(jd_content),
        "experience_requirements": _extract_experience_requirements(jd_content),
        "technical_requirements": _extract_technical_requirements(jd_content),
        "soft_skills": _extract_soft_skills(jd_content),
        "company_info": _extract_company_info(jd_content)
    }
    
    return analysis


@tool
def analyze_cv_content(cv_content: str) -> Dict[str, any]:
    """
    Analyze CV/Resume content to extract key information.
    
    Args:
        cv_content: CV/Resume text content
        
    Returns:
        Dict containing analyzed CV information
    """
    analysis = {
        "skills": _extract_cv_skills(cv_content),
        "experience": _extract_work_experience(cv_content),
        "education": _extract_education(cv_content),
        "projects": _extract_projects(cv_content),
        "certifications": _extract_certifications(cv_content),
        "achievements": _extract_achievements(cv_content),
        "years_of_experience": _calculate_experience_years(cv_content)
    }
    
    return analysis


def _extract_skills(content: str) -> List[str]:
    """Extract skills from job description."""
    skills = []
    
    # Common skill patterns
    skill_patterns = [
        r'(?:skills?|technologies?|tools?)[:\s]*([^.]+)',
        r'(?:experience with|proficiency in|knowledge of)[:\s]*([^.]+)',
        r'(?:must have|required)[:\s]*([^.]+)',
    ]
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # Split by common delimiters
            skill_items = re.split(r'[,;•\n]', match)
            for item in skill_items:
                skill = item.strip()
                if skill and len(skill) > 2:
                    skills.append(skill)
    
    return list(set(skills))[:20]  # Limit to top 20 unique skills


def _extract_responsibilities(content: str) -> List[str]:
    """Extract job responsibilities."""
    responsibilities = []
    
    # Look for responsibility sections
    resp_patterns = [
        r'(?:responsibilities?|duties?|role)[:\s]*([^.]+)',
        r'(?:you will|the candidate will)[:\s]*([^.]+)',
    ]
    
    for pattern in resp_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            resp_items = re.split(r'[•\n]', match)
            for item in resp_items:
                resp = item.strip()
                if resp and len(resp) > 10:
                    responsibilities.append(resp)
    
    return responsibilities[:10]  # Limit to top 10


def _extract_qualifications(content: str) -> List[str]:
    """Extract qualifications from job description."""
    qualifications = []
    
    qual_patterns = [
        r'(?:qualifications?|requirements?)[:\s]*([^.]+)',
        r'(?:minimum|preferred)[:\s]*([^.]+)',
    ]
    
    for pattern in qual_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            qual_items = re.split(r'[•\n]', match)
            for item in qual_items:
                qual = item.strip()
                if qual and len(qual) > 5:
                    qualifications.append(qual)
    
    return qualifications[:10]


def _extract_experience_requirements(content: str) -> str:
    """Extract experience requirements."""
    exp_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'minimum\s*(\d+)\s*years?',
        r'at least\s*(\d+)\s*years?'
    ]
    
    for pattern in exp_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return f"{match.group(1)} years"
    
    return "Not specified"


def _extract_technical_requirements(content: str) -> List[str]:
    """Extract technical requirements."""
    tech_keywords = [
        'programming', 'software', 'development', 'coding', 'algorithm',
        'database', 'api', 'framework', 'library', 'cloud', 'aws', 'azure',
        'docker', 'kubernetes', 'microservices', 'architecture'
    ]
    
    technical_reqs = []
    for keyword in tech_keywords:
        pattern = rf'[^.]*{keyword}[^.]*'
        matches = re.findall(pattern, content, re.IGNORECASE)
        technical_reqs.extend(matches)
    
    return list(set(technical_reqs))[:15]


def _extract_soft_skills(content: str) -> List[str]:
    """Extract soft skills from job description."""
    soft_skill_keywords = [
        'communication', 'leadership', 'teamwork', 'collaboration',
        'problem-solving', 'analytical', 'creative', 'adaptable',
        'organized', 'detail-oriented', 'self-motivated'
    ]
    
    soft_skills = []
    for skill in soft_skill_keywords:
        if re.search(rf'\b{skill}\b', content, re.IGNORECASE):
            soft_skills.append(skill.title())
    
    return soft_skills


def _extract_company_info(content: str) -> Dict[str, str]:
    """Extract company information."""
    company_info = {}
    
    # Try to extract company name (usually at the beginning)
    company_match = re.search(r'^([A-Z][a-zA-Z\s&.,]+)', content)
    if company_match:
        company_info['name'] = company_match.group(1).strip()
    
    # Extract industry information
    industry_keywords = ['technology', 'healthcare', 'finance', 'retail', 'manufacturing']
    for keyword in industry_keywords:
        if re.search(rf'\b{keyword}\b', content, re.IGNORECASE):
            company_info['industry'] = keyword.title()
            break
    
    return company_info


def _extract_cv_skills(content: str) -> List[str]:
    """Extract skills from CV."""
    skills = []
    
    # Look for skills section
    skill_section_match = re.search(r'(?:skills?|technologies?|competencies?)[:\s]*([^.]+)', content, re.IGNORECASE)
    if skill_section_match:
        skill_text = skill_section_match.group(1)
        skill_items = re.split(r'[,;•\n]', skill_text)
        for item in skill_items:
            skill = item.strip()
            if skill and len(skill) > 2:
                skills.append(skill)
    
    return list(set(skills))[:20]


def _extract_work_experience(content: str) -> List[Dict[str, str]]:
    """Extract work experience from CV."""
    experience = []
    
    # Look for experience patterns
    exp_patterns = [
        r'(\d{4})\s*-\s*(\d{4}|present|current)\s*[:\s]*([^.]+)',
        r'([A-Z][a-zA-Z\s&.,]+)\s*-\s*([A-Z][a-zA-Z\s]+)\s*\((\d{4})\s*-\s*(\d{4}|present)\)'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if len(match) >= 3:
                exp_entry = {
                    'period': f"{match[0]} - {match[1]}",
                    'description': match[2] if len(match) > 2 else ''
                }
                experience.append(exp_entry)
    
    return experience[:5]  # Limit to 5 most recent


def _extract_education(content: str) -> List[str]:
    """Extract education information."""
    education = []
    
    edu_patterns = [
        r'(?:bachelor|master|phd|degree)[^.]*',
        r'(?:university|college|institute)[^.]*',
        r'(?:b\.?s\.?|m\.?s\.?|ph\.?d\.?)[^.]*'
    ]
    
    for pattern in edu_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        education.extend(matches)
    
    return list(set(education))[:3]


def _extract_projects(content: str) -> List[str]:
    """Extract project information."""
    projects = []
    
    project_patterns = [
        r'(?:project|developed|built|created)[^.]*',
        r'(?:github|portfolio)[^.]*'
    ]
    
    for pattern in project_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        projects.extend(matches)
    
    return list(set(projects))[:5]


def _extract_certifications(content: str) -> List[str]:
    """Extract certifications."""
    certifications = []
    
    cert_patterns = [
        r'(?:certified|certification)[^.]*',
        r'(?:aws|azure|google cloud|oracle)[^.]*certified[^.]*'
    ]
    
    for pattern in cert_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        certifications.extend(matches)
    
    return list(set(certifications))[:5]


def _extract_achievements(content: str) -> List[str]:
    """Extract achievements and accomplishments."""
    achievements = []
    
    achievement_patterns = [
        r'(?:achieved|accomplished|awarded|recognized)[^.]*',
        r'(?:increased|improved|reduced|optimized)[^.]*\d+%[^.]*'
    ]
    
    for pattern in achievement_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        achievements.extend(matches)
    
    return list(set(achievements))[:5]


def _calculate_experience_years(content: str) -> int:
    """Calculate total years of experience."""
    years = []
    
    # Look for year ranges
    year_patterns = [
        r'(\d{4})\s*-\s*(\d{4})',
        r'(\d{4})\s*-\s*(?:present|current)'
    ]
    
    current_year = 2025  # Update as needed
    
    for pattern in year_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            start_year = int(match[0])
            end_year = current_year if match[1].lower() in ['present', 'current'] else int(match[1])
            years.append(end_year - start_year)
    
    return sum(years) if years else 0
