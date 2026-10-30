"""
AI Feedback, Project Recommendations, and Interview Prep Module
"""

from utils.skills_database import INTERVIEW_TIPS

def generate_ai_suggestions(parsed_data: dict, ats_score: int) -> list:
    """Generate smart, actionable AI suggestions tailored to candidate's resume."""
    suggestions = []
    text_lower = parsed_data.get("raw_text", "").lower()
    skills_flat = [s.lower() for s in parsed_data.get("skills_flat", [])]

    # 1. Technical Skills Check
    if len(skills_flat) < 8:
        suggestions.append("✔ Add more technical skills relevant to your target role (aim for 10+ core skills).")

    # 2. GitHub / Portfolio check
    if parsed_data.get("github") == "Not Found":
        suggestions.append("✔ Add your GitHub profile link to showcase code repositories and open-source contributions.")
    if parsed_data.get("portfolio") == "Not Found":
        suggestions.append("✔ Include a personal portfolio URL or live project demo links.")

    # 3. Measurable Achievements
    if not any(char in text_lower for char in ['%', '$', 'increased', 'decreased', 'reduced', 'improved']):
        suggestions.append("✔ Mention measurable achievements (e.g., 'Improved query response time by 40%', 'Handled 500+ records').")

    # 4. Certifications
    if not parsed_data.get("certifications"):
        suggestions.append("✔ Include industry certifications (e.g. AWS Certified, Coursera/Udemy Certificates, Power BI PL-300).")

    # 5. Internship / Experience
    if not parsed_data.get("experience"):
        suggestions.append("✔ Add internship experience or hands-on freelance / open-source work.")

    # 6. Specific Project Suggestions
    if "power bi" not in skills_flat and "tableau" not in skills_flat:
        suggestions.append("✔ Add a Power BI / Tableau dashboard project to demonstrate data visualization skills.")
    if "sql" not in skills_flat:
        suggestions.append("✔ Highlight complex SQL query expertise (JOINs, Window functions, CTEs).")

    # 7. Action verbs
    if "managed" not in text_lower and "spearheaded" not in text_lower and "developed" not in text_lower:
        suggestions.append("✔ Improve project descriptions using strong action verbs (e.g., Developed, Spearheaded, Engineered).")

    # Fallbacks if already high score
    if len(suggestions) < 3:
        suggestions.append("✔ Keep technical skills section organized into clear sub-categories.")
        suggestions.append("✔ Tailor top summary paragraph to match target job keywords.")

    return suggestions

def get_interview_prep_tips(user_skills_flat: list) -> dict:
    """Return tailored interview questions based on candidate's top skills."""
    tips = {}
    skills_lower = [s.lower() for s in user_skills_flat]

    for skill, question_list in INTERVIEW_TIPS.items():
        if skill in skills_lower:
            tips[skill.title()] = question_list

    if not tips:
        tips["General Technical Interview Tips"] = [
            "Be prepared to explain your core projects using the STAR method (Situation, Task, Action, Result).",
            "Review core data structure and algorithm complexity (Big O notation).",
            "Prepare 2-3 questions for the interviewer regarding team architecture and tools."
        ]

    return tips
