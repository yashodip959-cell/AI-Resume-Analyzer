"""
Job Recommender & Skill Gap Analysis Engine
Matches parsed resume skills against target job profiles.
"""

from utils.skills_database import JOB_BENCHMARKS

def recommend_jobs(parsed_skills_flat: list) -> list:
    """Recommend top job roles with match percentages based on candidate skills."""
    if not parsed_skills_flat:
        return []

    user_skills_lower = set([s.lower() for s in parsed_skills_flat])
    recommendations = []

    for role, benchmark in JOB_BENCHMARKS.items():
        req = set(benchmark["required_skills"])
        good = set(benchmark["good_to_have"])
        
        # Calculate weighted match
        req_match = len(user_skills_lower.intersection(req))
        good_match = len(user_skills_lower.intersection(good))
        
        total_possible = len(req) * 2 + len(good)
        score = (req_match * 2 + good_match) / total_possible * 100 if total_possible > 0 else 0
        match_percentage = min(round(score, 1), 100)

        missing_req = list(req - user_skills_lower)

        recommendations.append({
            "role": role,
            "match_percentage": match_percentage,
            "description": benchmark["description"],
            "missing_required_skills": [s.title() for s in missing_req],
            "req_count": len(req),
            "matched_req_count": req_match
        })

    # Sort by match percentage descending
    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
    return recommendations

def analyze_target_role_gap(target_role: str, user_skills_flat: list) -> dict:
    """Detailed skill gap analysis for a specific target role."""
    if target_role not in JOB_BENCHMARKS:
        target_role = "Data Analyst" # default fallback

    benchmark = JOB_BENCHMARKS[target_role]
    user_skills_lower = set([s.lower() for s in user_skills_flat])
    
    req_skills = benchmark["required_skills"]
    good_skills = benchmark["good_to_have"]

    present_skills = [s.title() for s in req_skills if s.lower() in user_skills_lower]
    missing_skills = [s.title() for s in req_skills if s.lower() not in user_skills_lower]
    bonus_missing = [s.title() for s in good_skills if s.lower() not in user_skills_lower]

    match_pct = round((len(present_skills) / len(req_skills)) * 100, 1) if req_skills else 0

    return {
        "target_role": target_role,
        "match_percentage": min(match_pct, 100),
        "present_skills": present_skills,
        "missing_skills": missing_skills,
        "bonus_recommended_skills": bonus_missing
    }
