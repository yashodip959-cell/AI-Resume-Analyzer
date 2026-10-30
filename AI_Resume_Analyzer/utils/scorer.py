"""
Multi-Factor ATS Resume Scorer Module (0 - 100)
Exact scoring breakdown matching specifications:
- Skills: 30
- Experience: 20
- Education: 15
- Projects: 10
- Certifications: 10
- Resume Formatting: 10
- Contact Info: 5
Total: 100
"""

from utils.ats_checker import check_ats_formatting

def calculate_ats_score(parsed_data: dict) -> dict:
    """Calculate granular breakdown of ATS score out of 100."""
    if not parsed_data:
        return {"total_score": 0, "breakdown": {}, "strength": "Needs Work", "completeness": 0}

    # 1. Skills (Max 30)
    skills_count = len(parsed_data.get("skills_flat", []))
    if skills_count >= 12:
        skills_score = 30
    elif skills_count >= 8:
        skills_score = 25
    elif skills_count >= 5:
        skills_score = 18
    elif skills_count >= 2:
        skills_score = 10
    else:
        skills_score = 5

    # 2. Experience (Max 20)
    exp = parsed_data.get("experience", [])
    raw_text = parsed_data.get("raw_text", "").lower()
    if len(exp) >= 3 or "senior" in raw_text or "lead" in raw_text or "manager" in raw_text:
        exp_score = 20
    elif len(exp) >= 1 or "experience" in raw_text or "intern" in raw_text:
        exp_score = 15
    elif "worked" in raw_text or "role" in raw_text:
        exp_score = 10
    else:
        exp_score = 5

    # 3. Education (Max 15)
    edu = parsed_data.get("education", [])
    if len(edu) >= 2 or any(d in ["bachelor", "master", "phd", "b.tech", "m.tech", "bca", "mca"] for d in [e.lower() for e in edu]):
        edu_score = 15
    elif len(edu) >= 1 or "degree" in raw_text or "university" in raw_text or "college" in raw_text:
        edu_score = 10
    else:
        edu_score = 5

    # 4. Projects (Max 10)
    projects = parsed_data.get("projects", [])
    if len(projects) >= 3 or "github" in parsed_data.get("github", "").lower():
        proj_score = 10
    elif len(projects) >= 1 or "built" in raw_text or "developed" in raw_text:
        proj_score = 7
    else:
        proj_score = 3

    # 5. Certifications (Max 10)
    certs = parsed_data.get("certifications", [])
    if len(certs) >= 2:
        cert_score = 10
    elif len(certs) >= 1:
        cert_score = 7
    else:
        cert_score = 2

    # 6. Resume Formatting (Max 10)
    formatting = check_ats_formatting(raw_text)
    format_score = int(formatting["score_out_of_10"])

    # 7. Contact Information (Max 5)
    contact_score = 0
    if parsed_data.get("email") != "Not Found":
        contact_score += 2
    if parsed_data.get("phone") != "Not Found":
        contact_score += 2
    if parsed_data.get("linkedin") != "Not Found" or parsed_data.get("github") != "Not Found":
        contact_score += 1
    contact_score = min(contact_score, 5)

    total_score = min(skills_score + exp_score + edu_score + proj_score + cert_score + format_score + contact_score, 100)

    # Determine Strength Rating
    if total_score >= 80:
        strength = "Outstanding ⭐⭐⭐"
    elif total_score >= 60:
        strength = "Good / Competitive ⭐⭐"
    else:
        strength = "Needs Improvement ⭐"

    # Completeness Percentage
    completeness = round(((skills_score/30 + exp_score/20 + edu_score/15 + proj_score/10 + cert_score/10 + format_score/10 + contact_score/5) / 7.0) * 100, 1)

    return {
        "total_score": total_score,
        "breakdown": {
            "Skills": {"score": skills_score, "max": 30},
            "Experience": {"score": exp_score, "max": 20},
            "Education": {"score": edu_score, "max": 15},
            "Projects": {"score": proj_score, "max": 10},
            "Certifications": {"score": cert_score, "max": 10},
            "Resume Formatting": {"score": format_score, "max": 10},
            "Contact Information": {"score": contact_score, "max": 5}
        },
        "strength": strength,
        "completeness": completeness,
        "ats_formatting_details": formatting["details"]
    }
