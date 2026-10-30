# 🚀 Professional AI Resume Analyzer

Competition-grade **AI Resume Analyzer** web application built using **Python, Streamlit, SQLite, Plotly, ReportLab, and NLP techniques**.

---

## 📂 Project Structure

```text
AI_Resume_Analyzer/
│
├── app.py                      # Main Streamlit dashboard application UI
├── requirements.txt            # All required Python packages
├── README.md                   # Setup guide & running instructions
│
├── assets/
│   ├── logo.png                # App branding logo
│   ├── generate_logo.py        # Logo generator script
│   └── style.css               # Custom CSS Glassmorphism theme
│
├── utils/
│   ├── __init__.py
│   ├── pdf_reader.py          # Extractor for PDF & DOCX
│   ├── parser.py              # Regex + NLP extractor (Contact, Skills, Education, Experience, etc.)
│   ├── scorer.py              # Multi-factor ATS Scorer (0-100) & strength meter
│   ├── charts.py              # Plotly Gauge, Donut, Bar, Radar charts
│   ├── report.py              # ReportLab PDF & TXT report generator
│   ├── ats_checker.py         # ATS formatting and readability checker
│   ├── keyword_matcher.py     # Job Description vs Resume TF-IDF keyword matcher
│   ├── job_recommender.py     # Role matching & career recommendation engine
│   ├── ai_feedback.py         # Smart actionable feedback & interview prep tips
│   └── skills_database.py     # Skill benchmarks & interview database
│
├── database/
│   ├── resume_history.db       # SQLite database file
│   └── database.py             # SQLite CRUD operations
│
├── reports/                    # Generated PDF/TXT reports folder
│   ├── Resume_Report.pdf
│   └── Resume_Report.txt
│
└── sample_resumes/             # Pre-built sample resumes for quick demo
    ├── sample1.pdf             # Data Analyst Sample Resume
    ├── sample2.pdf             # Python Developer Sample Resume
    └── sample3.pdf             # Business Analyst Sample Resume
```

---

## ⚡ How to Install & Run Project (Project Kasa Run Karaycha)

### Step 1: Open Terminal in Project Folder
Navigate to the project directory:
```bash
cd C:\Users\dhanshree\.gemini\antigravity\scratch\AI_Resume_Analyzer
```

### Step 2: Install Required Dependencies
Run the command to install all libraries:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Streamlit Application
Start the application using:
```bash
streamlit run app.py
```

After running this command, Streamlit will automatically open your web browser at:
`http://localhost:8501`

---

## ⭐ Core Features Included

1. **📄 Multi-Format Resume Parsing**: Parses Name, Email, Phone, LinkedIn, GitHub, Portfolio, Technical Skills, Education, Experience, Projects, Certifications, Languages.
2. **📊 Granular ATS Scoring (0 - 100)**: 7-part weighted breakdown (Skills, Experience, Education, Projects, Certifications, Formatting, Contact info).
3. **📈 Interactive Charts**: ATS Gauge Chart, Skill Donut Chart, Score Breakdown Bar Chart, Technical Radar Chart.
4. **🎯 Job Description Matcher**: Paste any JD to compute match %, matched keywords, and missing keywords.
5. **💼 Career Job Recommender & Skill Gap Analysis**: Benchmark against Data Analyst, Data Scientist, Python Developer, BI Developer, etc.
6. **📜 SQLite History & Resume Comparison**: Store history, compare score progress of 2 uploads side-by-side.
7. **📑 Downloadable Reports**: Export publication-quality **PDF** & **TXT** audit reports.
8. **💡 Interview Preparation Tips**: Tailored technical questions based on top candidate skills.
