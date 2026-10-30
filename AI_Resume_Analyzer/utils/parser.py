"""
Resume Content Parser Module
Extracts Contact Info, Skills, Education, Experience, Projects, Certifications, Links.
"""

import re
from utils.skills_database import SKILL_CATEGORIES

def extract_email(text: str) -> str:
    """Extract email address using regex."""
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else "Not Found"

def extract_phone(text: str) -> str:
    """Extract phone number using regex patterns."""
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else "Not Found"

def extract_links(text: str) -> dict:
    """Extract LinkedIn, GitHub, Portfolio, and social URLs."""
    linkedin = "Not Found"
    github = "Not Found"
    portfolio = "Not Found"

    # LinkedIn
    li_match = re.search(r'(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)', text, re.IGNORECASE)
    if li_match:
        linkedin = li_match.group(0)
    elif "linkedin.com" in text.lower():
        linkedin = "LinkedIn Profile Present"

    # GitHub
    gh_match = re.search(r'(https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+)', text, re.IGNORECASE)
    if gh_match:
        github = gh_match.group(0)
    elif "github.com" in text.lower() or "github" in text.lower():
        github = "GitHub Profile Present"

    # Portfolio / Websites
    urls = re.findall(r'https?://[^\s,]+', text)
    for url in urls:
        if "linkedin" not in url.lower() and "github" not in url.lower():
            portfolio = url
            break

    return {
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio
    }

def extract_name(text: str) -> str:
    """Extract candidate name from header lines."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "Candidate Name"
    
    # Check first 3 lines for a probable name (non-email, non-phone, clean text)
    for line in lines[:3]:
        if not re.search(r'(@|phone|email|resume|cv|curriculum|\+?\d{10})', line, re.IGNORECASE):
            # Clean non-alphabetical headers
            clean_name = re.sub(r'[^a-zA-Z\s\.]', '', line).strip()
            if 2 <= len(clean_name.split()) <= 4:
                return clean_name.title()

    return lines[0].title()[:30]

def extract_skills(text: str) -> dict:
    """Categorize and extract skills found in the text."""
    found_skills = {}
    all_found_flat = set()
    text_lower = text.lower()

    for category, skill_list in SKILL_CATEGORIES.items():
        found_in_cat = []
        for skill in skill_list:
            # Word boundary search for accurate match
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_in_cat.append(skill.title())
                all_found_flat.add(skill.lower())
        if found_in_cat:
            found_skills[category] = found_in_cat

    return {
        "categorized": found_skills,
        "flat_list": sorted(list(all_found_flat))
    }

def extract_sections(text: str) -> dict:
    """Extract sections: Education, Experience, Projects, Certifications, Languages."""
    text_lower = text.lower()
    
    sections = {
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "languages": []
    }

    # Education keywords & degree detection
    degrees = ["bachelor", "master", "b.tech", "m.tech", "b.e", "m.e", "b.sc", "m.sc", "bca", "mca", "phd", "diploma", "degree", "university", "college", "institute"]
    for deg in degrees:
        if deg in text_lower:
            sections["education"].append(deg.upper() if len(deg) <= 4 else deg.title())
    sections["education"] = list(set(sections["education"]))

    # Experience detection
    exp_matches = re.findall(r'(\d+\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience)', text_lower)
    exp_roles = re.findall(r'\b(developer|analyst|engineer|intern|manager|lead|consultant|architect|specialist)\b', text_lower)
    sections["experience"] = exp_matches + [r.title() for r in set(exp_roles)]

    # Projects detection
    if "project" in text_lower or "portfolio" in text_lower:
        proj_lines = [line for line in text.split('\n') if 'project' in line.lower() or 'dashboard' in line.lower() or 'built' in line.lower() or 'developed' in line.lower()]
        sections["projects"] = [p.strip() for p in proj_lines[:5]]

    # Certifications detection
    certs = ["certified", "certification", "aws", "azure", "google", "coursera", "udemy", "nptel", "ibm", "microsoft"]
    for cert in certs:
        if cert in text_lower:
            sections["certifications"].append(cert.title())
    sections["certifications"] = list(set(sections["certifications"]))

    # Languages detection
    langs = ["english", "hindi", "marathi", "german", "french", "spanish", "japanese", "mandarin"]
    for lang in langs:
        if lang in text_lower:
            sections["languages"].append(lang.title())

    return sections

def parse_resume(raw_text: str) -> dict:
    """Master parse function combining all extractions."""
    if not raw_text.strip():
        return {}

    name = extract_name(raw_text)
    email = extract_email(raw_text)
    phone = extract_phone(raw_text)
    links = extract_links(raw_text)
    skills = extract_skills(raw_text)
    sections = extract_sections(raw_text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": links["linkedin"],
        "github": links["github"],
        "portfolio": links["portfolio"],
        "skills": skills["categorized"],
        "skills_flat": skills["flat_list"],
        "education": sections["education"],
        "experience": sections["experience"],
        "projects": sections["projects"],
        "certifications": sections["certifications"],
        "languages": sections["languages"],
        "raw_text": raw_text
    }
