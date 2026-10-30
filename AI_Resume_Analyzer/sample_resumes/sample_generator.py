"""
Script to generate sample resumes (PDF) for out-of-the-box demo testing.
Creates sample1.pdf (Data Analyst), sample2.pdf (Python Developer), sample3.pdf (Business Analyst).
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

SAMPLE_DIR = os.path.dirname(__file__)

def generate_samples():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#2B6CB0'))
    sub_style = ParagraphStyle('SubHeader', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#2D3748'))
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)

    # Sample 1: Data Analyst
    doc1 = SimpleDocTemplate(os.path.join(SAMPLE_DIR, "sample1.pdf"), pagesize=letter)
    s1 = [
        Paragraph("<b>RAHUL SHARMA</b>", header_style),
        Paragraph("Email: rahul.sharma@example.com | Phone: +91 9876543210 | LinkedIn: linkedin.com/in/rahul-sharma | GitHub: github.com/rahul-sharma", body_style),
        HRFlowable(width="100%", thickness=1, color=colors.gray, spaceBefore=5, spaceAfter=10),
        Paragraph("<b>PROFESSIONAL SUMMARY</b>", sub_style),
        Paragraph("Detail-oriented Data Analyst with 3+ years of experience in data analysis, SQL querying, Power BI dashboard development, and predictive modeling using Python and pandas.", body_style),
        Spacer(1, 10),
        Paragraph("<b>TECHNICAL SKILLS</b>", sub_style),
        Paragraph("• Programming: Python, SQL, R<br/>• Data & BI: Power BI, Tableau, Excel, Pandas, NumPy, Scikit-Learn<br/>• Databases: MySQL, PostgreSQL, Snowflake", body_style),
        Spacer(1, 10),
        Paragraph("<b>WORK EXPERIENCE</b>", sub_style),
        Paragraph("<b>Senior Data Analyst</b> - TechCorp Analytics (2022 - Present)<br/>• Analyzed customer churn data for 50,000+ users using Python and SQL.<br/>• Built interactive Power BI dashboards that increased reporting efficiency by 35%.<br/>• Spearheaded automated ETL pipelines using SQL procedures.", body_style),
        Spacer(1, 10),
        Paragraph("<b>PROJECTS</b>", sub_style),
        Paragraph("<b>E-Commerce Sales Insights Dashboard</b><br/>• Developed a Power BI dashboard visualizing sales trends across 10+ regions.<br/>• Achieved 25% optimization in inventory forecasting.", body_style),
        Spacer(1, 10),
        Paragraph("<b>EDUCATION & CERTIFICATIONS</b>", sub_style),
        Paragraph("• B.Tech in Computer Science - Pune University (2018 - 2022)<br/>• Microsoft Certified: Power BI Data Analyst Associate (PL-300)", body_style)
    ]
    doc1.build(s1)

    # Sample 2: Python Developer
    doc2 = SimpleDocTemplate(os.path.join(SAMPLE_DIR, "sample2.pdf"), pagesize=letter)
    s2 = [
        Paragraph("<b>PRIYA PATEL</b>", header_style),
        Paragraph("Email: priya.patel@example.com | Phone: +91 9123456789 | GitHub: github.com/priya-patel", body_style),
        HRFlowable(width="100%", thickness=1, color=colors.gray, spaceBefore=5, spaceAfter=10),
        Paragraph("<b>PROFESSIONAL SUMMARY</b>", sub_style),
        Paragraph("Passionate Python & Full Stack Backend Developer with expertise in Django, Flask, FastAPI, Docker, and REST APIs.", body_style),
        Spacer(1, 10),
        Paragraph("<b>TECHNICAL SKILLS</b>", sub_style),
        Paragraph("• Languages: Python, JavaScript, SQL, C++<br/>• Web & Backend: Django, Flask, FastAPI, React, Node.js<br/>• DevOps & DB: Docker, AWS, Git, PostgreSQL, Redis", body_style),
        Spacer(1, 10),
        Paragraph("<b>WORK EXPERIENCE</b>", sub_style),
        Paragraph("<b>Python Backend Developer</b> - CloudSolutions Inc (2021 - Present)<br/>• Architected scalable microservices using Python FastAPI and PostgreSQL.<br/>• Reduced API latency by 45% using Redis caching and AsyncIO.", body_style),
        Spacer(1, 10),
        Paragraph("<b>EDUCATION</b>", sub_style),
        Paragraph("• B.E. in Information Technology - Mumbai University", body_style)
    ]
    doc2.build(s2)

    # Sample 3: Business Analyst
    doc3 = SimpleDocTemplate(os.path.join(SAMPLE_DIR, "sample3.pdf"), pagesize=letter)
    s3 = [
        Paragraph("<b>AMIT VERMA</b>", header_style),
        Paragraph("Email: amit.verma@example.com | Phone: +91 9988776655 | LinkedIn: linkedin.com/in/amit-verma", body_style),
        HRFlowable(width="100%", thickness=1, color=colors.gray, spaceBefore=5, spaceAfter=10),
        Paragraph("<b>PROFESSIONAL SUMMARY</b>", sub_style),
        Paragraph("Results-driven Business Analyst skilled in Excel, Agile, Scrum, Requirements Gathering, and SQL.", body_style),
        Spacer(1, 10),
        Paragraph("<b>SKILLS</b>", sub_style),
        Paragraph("• Analytical: Business Analysis, Agile, Scrum, Jira, Documentation<br/>• Tools: Advanced Excel, SQL, Power BI, Communication, Leadership", body_style),
        Spacer(1, 10),
        Paragraph("<b>EDUCATION</b>", sub_style),
        Paragraph("• MBA in Business Analytics - Delhi University", body_style)
    ]
    doc3.build(s3)

    print("Sample resumes generated successfully.")

if __name__ == "__main__":
    generate_samples()
