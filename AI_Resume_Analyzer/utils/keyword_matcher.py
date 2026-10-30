"""
Job Description Keyword Matcher & Gap Analysis Engine
Computes similarity %, matched keywords, missing keywords, and keyword density.
"""

import re

def extract_keywords(text: str) -> list:
    """Extract candidate keywords (alphanumeric terms, ignoring stop words)."""
    stop_words = {
        "and", "the", "to", "for", "in", "of", "with", "a", "an", "is", "at", 
        "by", "from", "on", "or", "as", "be", "are", "this", "that", "it", "have",
        "has", "will", "can", "work", "experience", "looking", "candidate", "role",
        "job", "team", "years", "skills", "ability", "knowledge", "strong"
    }
    words = re.findall(r'\b[a-zA-Z0-9+#\.\-]{2,}\b', text.lower())
    return [w for w in words if w not in stop_words and not w.isdigit()]

def match_job_description(resume_text: str, job_description: str) -> dict:
    """Compute JD match %, matched keywords, missing keywords, and similarity breakdown."""
    if not resume_text or not job_description:
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "keyword_density": {}
        }

    jd_words = extract_keywords(job_description)
    res_words = set(extract_keywords(resume_text))

    if not jd_words:
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "keyword_density": {}
        }

    # Frequency count in JD
    jd_freq = {}
    for word in jd_words:
        jd_freq[word] = jd_freq.get(word, 0) + 1

    # Sort high-priority keywords from JD
    sorted_jd_terms = [item[0] for item in sorted(jd_freq.items(), key=lambda x: x[1], reverse=True)]

    matched = []
    missing = []

    for term in sorted_jd_terms[:40]:
        if term in res_words:
            matched.append(term)
        else:
            missing.append(term)

    total_top_terms = len(sorted_jd_terms[:40])
    match_pct = round((len(matched) / total_top_terms) * 100, 1) if total_top_terms > 0 else 0

    return {
        "match_percentage": match_pct,
        "matched_keywords": [m.title() for m in matched[:20]],
        "missing_keywords": [m.title() for m in missing[:20]],
        "jd_top_terms_count": total_top_terms,
        "matched_count": len(matched)
    }
