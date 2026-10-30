"""
ATS Formatting & Readability Checker
Evaluates formatting, standard section headers, action verbs, and ATS friendliness.
"""

import re

ACTION_VERBS = [
    "achieved", "analyzed", "architected", "automated", "built", "created", 
    "designed", "developed", "engineered", "established", "executed", 
    "implemented", "improved", "increased", "led", "managed", "optimized", 
    "orchestrated", "reduced", "spearheaded", "transformed"
]

STANDARD_SECTIONS = [
    "education", "experience", "work history", "projects", "skills", 
    "certifications", "summary", "objective"
]

def check_ats_formatting(text: str) -> dict:
    """Analyze text for ATS friendly rules and structure."""
    text_lower = text.lower()
    checks = []

    # 1. Email check
    has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))
    checks.append({
        "rule": "Contact Info (Email)",
        "passed": has_email,
        "detail": "Valid email address found." if has_email else "Missing email address!"
    })

    # 2. Phone check
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
    checks.append({
        "rule": "Contact Info (Phone)",
        "passed": has_phone,
        "detail": "Phone number included." if has_phone else "Missing phone number!"
    })

    # 3. Action verbs count
    verbs_found = [verb for verb in ACTION_VERBS if verb in text_lower]
    has_verbs = len(verbs_found) >= 3
    checks.append({
        "rule": "Strong Action Verbs",
        "passed": has_verbs,
        "detail": f"Found {len(verbs_found)} action verbs ({', '.join(verbs_found[:5])})" if has_verbs else "Low usage of strong action verbs!"
    })

    # 4. Standard section headers
    found_headers = [sec for sec in STANDARD_SECTIONS if sec in text_lower]
    has_headers = len(found_headers) >= 3
    checks.append({
        "rule": "Standard Section Headings",
        "passed": has_headers,
        "detail": f"Found sections: {', '.join([h.title() for h in found_headers])}" if has_headers else "Non-standard section headers used!"
    })

    # 5. Length & Word Count Check
    word_count = len(text.split())
    ideal_length = 250 <= word_count <= 1200
    checks.append({
        "rule": "Optimal Word Count (250 - 1200 words)",
        "passed": ideal_length,
        "detail": f"Current word count: {word_count} words." if ideal_length else f"Word count ({word_count}) is too short or too long."
    })

    # 6. Quantifiable achievements (Numbers & percentages)
    metrics_found = re.findall(r'\b\d+%\b|\$\d+|\b\d+\+\b', text)
    has_metrics = len(metrics_found) >= 1
    checks.append({
        "rule": "Quantifiable Achievements (Metrics & %)",
        "passed": has_metrics,
        "detail": f"Found metrics: {', '.join(metrics_found[:5])}" if has_metrics else "Include measurable metrics (e.g. Improved by 30%, 5+ projects)."
    })

    passed_count = sum(1 for c in checks if c["passed"])
    score_out_of_10 = round((passed_count / len(checks)) * 10, 1)

    return {
        "score_out_of_10": score_out_of_10,
        "passed_rules": passed_count,
        "total_rules": len(checks),
        "details": checks
    }
