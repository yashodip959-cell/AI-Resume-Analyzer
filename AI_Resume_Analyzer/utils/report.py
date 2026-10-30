"""
Professional PDF & TXT Resume Report Generator using ReportLab
Generates styled PDF audit reports and downloadable text reports.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(parsed_data: dict, scoring_res: dict, recommendations: list, suggestions: list) -> str:
    """Generate a clean, professional PDF report file."""
    pdf_path = os.path.join(REPORTS_DIR, "Resume_Report.pdf")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#6C5CE7'),
        alignment=0,
        spaceAfter=10
    )
    
    heading2_style = ParagraphStyle(
        'DocSubHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4A5568')
    )

    # 1. Header
    story.append(Paragraph("<b>AI RESUME ANALYZER AUDIT REPORT</b>", title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#6C5CE7'), spaceAfter=15))

    # 2. Candidate Overview Table
    name = parsed_data.get("name", "Candidate")
    email = parsed_data.get("email", "N/A")
    phone = parsed_data.get("phone", "N/A")
    total_score = scoring_res.get("total_score", 0)
    strength = scoring_res.get("strength", "N/A")

    candidate_info = [
        [Paragraph("<b>Candidate Name:</b>", body_style), Paragraph(name, body_style)],
        [Paragraph("<b>Email:</b>", body_style), Paragraph(email, body_style)],
        [Paragraph("<b>Phone:</b>", body_style), Paragraph(phone, body_style)],
        [Paragraph("<b>Overall ATS Score:</b>", body_style), Paragraph(f"<b>{total_score} / 100</b> ({strength})", body_style)]
    ]

    t_info = Table(candidate_info, colWidths=[130, 400])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#EDF2F7')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))

    # 3. Score Breakdown
    story.append(Paragraph("<b>ATS Score Breakdown</b>", heading2_style))
    breakdown_data = [["Category", "Earned Score", "Max Points"]]
    for cat, val in scoring_res.get("breakdown", {}).items():
        breakdown_data.append([cat, str(val["score"]), str(val["max"])])

    t_breakdown = Table(breakdown_data, colWidths=[250, 140, 140])
    t_breakdown.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#6C5CE7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_breakdown)
    story.append(Spacer(1, 15))

    # 4. Top Skill Recommendations & AI Feedback
    story.append(Paragraph("<b>AI Actionable Suggestions</b>", heading2_style))
    for sug in suggestions[:6]:
        story.append(Paragraph(f"• {sug}", body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # 5. Top Job Recommendations
    story.append(Paragraph("<b>Top Career Job Matches</b>", heading2_style))
    job_table_data = [["Job Role", "Match %", "Key Missing Skill Requirements"]]
    for rec in recommendations[:4]:
        missing_str = ", ".join(rec.get("missing_required_skills", [])[:3]) or "All required skills met!"
        job_table_data.append([rec["role"], f"{rec['match_percentage']}%", missing_str])

    t_jobs = Table(job_table_data, colWidths=[150, 80, 300])
    t_jobs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2D3748')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_jobs)

    doc.build(story)
    return pdf_path

def generate_txt_report(parsed_data: dict, scoring_res: dict, recommendations: list, suggestions: list) -> str:
    """Generate a clean TXT summary report file."""
    txt_path = os.path.join(REPORTS_DIR, "Resume_Report.txt")
    
    name = parsed_data.get("name", "Candidate")
    email = parsed_data.get("email", "N/A")
    phone = parsed_data.get("phone", "N/A")
    total_score = scoring_res.get("total_score", 0)

    lines = [
        "==================================================",
        "          AI RESUME ANALYZER AUDIT REPORT         ",
        "==================================================",
        f"Candidate Name: {name}",
        f"Email         : {email}",
        f"Phone         : {phone}",
        f"Overall Score : {total_score} / 100",
        f"Strength      : {scoring_res.get('strength', 'N/A')}",
        "--------------------------------------------------",
        "SCORE BREAKDOWN:",
    ]

    for cat, val in scoring_res.get("breakdown", {}).items():
        lines.append(f"  - {cat:<22}: {val['score']} / {val['max']}")

    lines.append("--------------------------------------------------")
    lines.append("AI IMPROVEMENT SUGGESTIONS:")
    for sug in suggestions:
        lines.append(f"  {sug}")

    lines.append("--------------------------------------------------")
    lines.append("TOP JOB RECOMMENDATIONS:")
    for rec in recommendations:
        lines.append(f"  - {rec['role']:<20}: {rec['match_percentage']}% Match")

    lines.append("==================================================")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return txt_path
