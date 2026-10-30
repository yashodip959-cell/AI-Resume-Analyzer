"""
====================================================================
           AI RESUME ANALYZER - STREAMLIT DASHBOARD
           Full Competition-Grade Python Application
====================================================================
"""

import streamlit as st
import pandas as pd
import os
import json

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer 🚀",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports from project modules
from utils.pdf_reader import extract_resume_text
from utils.parser import parse_resume
from utils.scorer import calculate_ats_score
from utils.charts import (
    create_ats_gauge_chart,
    create_skill_donut_chart,
    create_score_breakdown_bar,
    create_skill_radar_chart
)
from utils.keyword_matcher import match_job_description
from utils.job_recommender import recommend_jobs, analyze_target_role_gap
from utils.ai_feedback import generate_ai_suggestions, get_interview_prep_tips
from utils.report import generate_pdf_report, generate_txt_report
from database.database import (
    init_db,
    insert_resume_record,
    get_all_resumes,
    get_resume_by_id,
    delete_resume_record
)

# Initialize Database
init_db()

# Load Custom CSS
CSS_PATH = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App Logo
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

# Sidebar Configuration
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=110)
    
    st.title("AI Resume Analyzer")
    st.markdown("---")
    
    app_mode = st.radio(
        "📌 Navigation",
        [
            "📄 Resume Analyzer",
            "🎯 JD Keyword Matcher",
            "⚖️ Resume Comparison",
            "📜 History & Analytics",
            "💡 Interview Prep Tips"
        ]
    )

    st.markdown("---")
    target_role = st.selectbox(
        "🎯 Target Job Role Benchmark",
        [
            "Data Analyst",
            "Data Scientist",
            "BI Developer",
            "Python Developer",
            "Full Stack Developer",
            "Business Analyst",
            "AI / Machine Learning Engineer"
        ]
    )

    st.markdown("---")
    theme_mode = st.toggle("🌙 Dark Mode Custom Palette", value=True)
    st.info("💡 **Competition Tip:** Upload a PDF or select a sample resume to test parsing, ATS scoring, and PDF report export!")

# Main Dashboard Title
st.markdown("<h1 style='text-align: center; color: #6C5CE7;'>🚀 Professional AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'>Upload your Resume (PDF/DOCX) to get instant ATS Scores, Skill Gap Analysis, Job Recommendations, and Downloadable PDF Reports.</p>", unsafe_allow_html=True)
st.markdown("---")

# Session State Storage
if "current_parsed" not in st.session_state:
    st.session_state.current_parsed = None
if "current_scoring" not in st.session_state:
    st.session_state.current_scoring = None
if "current_raw_text" not in st.session_state:
    st.session_state.current_raw_text = ""

# Sample Resumes Selector
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_resumes")
sample_files = [f for f in os.listdir(SAMPLE_DIR) if f.endswith(".pdf")] if os.path.exists(SAMPLE_DIR) else []

# ====================================================================
# MODE 1: RESUME ANALYZER
# ====================================================================
if app_mode == "📄 Resume Analyzer":
    col_up1, col_up2 = st.columns([2, 1])

    with col_up1:
        uploaded_file = st.file_uploader(
            "📥 Upload Resume (PDF or DOCX)",
            type=["pdf", "docx"],
            help="Select a PDF or DOCX file to analyze."
        )

    with col_up2:
        st.markdown("**Or Try Demo Sample Resumes:**")
        selected_sample = st.selectbox("Select Sample Resume", ["None"] + sample_files)

    raw_text = ""
    file_to_parse = None

    if uploaded_file is not None:
        file_to_parse = uploaded_file
    elif selected_sample != "None":
        file_to_parse = os.path.join(SAMPLE_DIR, selected_sample)

    if file_to_parse is not None:
        with st.spinner("⚡ Processing resume with AI NLP parsing engine..."):
            raw_text = extract_resume_text(file_to_parse)
            if raw_text:
                parsed_data = parse_resume(raw_text)
                scoring_res = calculate_ats_score(parsed_data)
                
                st.session_state.current_parsed = parsed_data
                st.session_state.current_scoring = scoring_res
                st.session_state.current_raw_text = raw_text

                # Save record to Database History
                rec_jobs = recommend_jobs(parsed_data.get("skills_flat", []))
                sug_list = generate_ai_suggestions(parsed_data, scoring_res["total_score"])
                pdf_p = generate_pdf_report(parsed_data, scoring_res, rec_jobs, sug_list)
                txt_p = generate_txt_report(parsed_data, scoring_res, rec_jobs, sug_list)

                insert_resume_record(parsed_data, scoring_res, target_role=target_role, pdf_path=pdf_p, txt_path=txt_p)
                st.success("✅ Resume parsed and saved to SQLite History database!")
            else:
                st.error("⚠️ Unable to extract text from the selected document.")

    if st.session_state.current_parsed:
        parsed_data = st.session_state.current_parsed
        scoring_res = st.session_state.current_scoring

        # Top Executive Metrics Row
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)

        with mcol1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">ATS Score (100)</div>
                    <div class="metric-value">{scoring_res['total_score']} / 100</div>
                    <div class="metric-subtitle">Overall Rating</div>
                </div>
            """, unsafe_allow_html=True)

        with mcol2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Resume Strength</div>
                    <div class="metric-value" style="font-size: 20px;">{scoring_res['strength']}</div>
                    <div class="metric-subtitle">Evaluated Level</div>
                </div>
            """, unsafe_allow_html=True)

        with mcol3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Completeness Score</div>
                    <div class="metric-value">{scoring_res['completeness']}%</div>
                    <div class="metric-subtitle">Structure Index</div>
                </div>
            """, unsafe_allow_html=True)

        with mcol4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Target Role Fit</div>
                    <div class="metric-value" style="font-size: 20px; color: #55E6C1;">{target_role}</div>
                    <div class="metric-subtitle">Benchmark Selected</div>
                </div>
            """, unsafe_allow_html=True)

        # Tabbed Details
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Charts & Visuals",
            "👤 Parsed Profile",
            "🤖 AI Feedback & Suggestions",
            "🎯 Job Recommendations",
            "📑 Download Reports"
        ])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(create_ats_gauge_chart(scoring_res['total_score']), use_container_width=True)
                st.plotly_chart(create_score_breakdown_bar(scoring_res['breakdown']), use_container_width=True)
            with c2:
                st.plotly_chart(create_skill_donut_chart(parsed_data.get('skills', {})), use_container_width=True)
                st.plotly_chart(create_skill_radar_chart(parsed_data.get('skills_flat', [])), use_container_width=True)

        with tab2:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.subheader("📌 Contact Details")
                st.write(f"**Name:** {parsed_data.get('name')}")
                st.write(f"**Email:** {parsed_data.get('email')}")
                st.write(f"**Phone:** {parsed_data.get('phone')}")
                st.write(f"**LinkedIn:** {parsed_data.get('linkedin')}")
                st.write(f"**GitHub:** {parsed_data.get('github')}")
                st.write(f"**Portfolio:** {parsed_data.get('portfolio')}")

                st.subheader("🎓 Education & Academics")
                edu_list = parsed_data.get("education", [])
                if edu_list:
                    for e in edu_list:
                        st.write(f"• {e}")
                else:
                    st.write("No explicit education records detected.")

            with col_p2:
                st.subheader("🛠 Technical & Soft Skills")
                categorized = parsed_data.get("skills", {})
                if categorized:
                    for cat, s_list in categorized.items():
                        st.write(f"**{cat}:**")
                        chips_html = "".join([f'<span class="skill-chip">{s}</span>' for s in s_list])
                        st.markdown(chips_html, unsafe_allow_html=True)
                        st.write("")
                else:
                    st.write("No categorized skills detected.")

                st.subheader("📜 Certifications & Projects")
                st.write("**Certifications:** " + (", ".join(parsed_data.get("certifications", [])) or "None"))
                st.write("**Detected Projects:**")
                for p in parsed_data.get("projects", [])[:4]:
                    st.write(f"• {p}")

        with tab3:
            st.subheader("🤖 Smart Actionable AI Suggestions")
            sug_list = generate_ai_suggestions(parsed_data, scoring_res["total_score"])
            for sug in sug_list:
                st.success(sug)

            st.subheader("📋 ATS Formatting & Readability Checks")
            for detail in scoring_res.get("ats_formatting_details", []):
                if detail["passed"]:
                    st.markdown(f"✅ **{detail['rule']}**: {detail['detail']}")
                else:
                    st.markdown(f"❌ **{detail['rule']}**: {detail['detail']}")

        with tab4:
            st.subheader(f"🎯 Target Role Skill Gap Analysis ({target_role})")
            gap = analyze_target_role_gap(target_role, parsed_data.get("skills_flat", []))
            
            gc1, gc2 = st.columns(2)
            with gc1:
                st.metric("Benchmark Role Match", f"{gap['match_percentage']}%")
                st.write("**Present Benchmark Skills:**")
                for ps in gap["present_skills"]:
                    st.markdown(f"✅ {ps}")
            with gc2:
                st.write("**Missing Required Skills:**")
                for ms in gap["missing_skills"]:
                    st.markdown(f"❌ <span style='color:#FF7675; font-weight:bold;'>{ms}</span>", unsafe_allow_html=True)
                st.write("**Good-to-have Recommended Skills:**")
                for bs in gap["bonus_recommended_skills"]:
                    st.markdown(f"⚡ {bs}")

            st.markdown("---")
            st.subheader("💼 Top Recommended Job Matches")
            recs = recommend_jobs(parsed_data.get("skills_flat", []))
            rec_df = pd.DataFrame(recs)
            if not rec_df.empty:
                st.dataframe(
                    rec_df[["role", "match_percentage", "description"]],
                    column_config={
                        "role": "Recommended Job Role",
                        "match_percentage": st.column_config.NumberColumn("Match %", format="%.1f%%"),
                        "description": "Role Summary"
                    },
                    use_container_width=True
                )

        with tab5:
            st.subheader("📥 Export & Download Audit Reports")
            rec_jobs = recommend_jobs(parsed_data.get("skills_flat", []))
            sug_list = generate_ai_suggestions(parsed_data, scoring_res["total_score"])
            
            pdf_path = generate_pdf_report(parsed_data, scoring_res, rec_jobs, sug_list)
            txt_path = generate_txt_report(parsed_data, scoring_res, rec_jobs, sug_list)

            dcol1, dcol2 = st.columns(2)

            with dcol1:
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pf:
                        st.download_button(
                            label="📄 Download Full PDF Report",
                            data=pf,
                            file_name="Resume_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

            with dcol2:
                if os.path.exists(txt_path):
                    with open(txt_path, "rb") as tf:
                        st.download_button(
                            label="📝 Download Text Report (TXT)",
                            data=tf,
                            file_name="Resume_Report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

# ====================================================================
# MODE 2: JOB DESCRIPTION MATCHER
# ====================================================================
elif app_mode == "🎯 JD Keyword Matcher":
    st.subheader("🎯 Job Description Keyword & ATS Optimization Matcher")
    st.write("Paste a target job description below to check keyword match percentage and missing keywords.")

    jd_text = st.text_area("Paste Job Description (JD) Here:", height=200)

    if st.button("🚀 Analyze JD Match", use_container_width=True):
        if not st.session_state.current_raw_text:
            st.warning("⚠️ Please upload a resume first under the '📄 Resume Analyzer' tab!")
        elif not jd_text.strip():
            st.warning("⚠️ Please paste a valid job description.")
        else:
            match_res = match_job_description(st.session_state.current_raw_text, jd_text)
            
            jcol1, jcol2 = st.columns(2)
            with jcol1:
                st.metric("JD Match Percentage", f"{match_res['match_percentage']}%")
                st.write("**Matched Keywords:**")
                for mk in match_res["matched_keywords"]:
                    st.markdown(f"✅ {mk}")

            with jcol2:
                st.write("**Missing High-Priority Keywords:**")
                for ek in match_res["missing_keywords"]:
                    st.markdown(f"❌ <span style='color:#FF7675;'>{ek}</span>", unsafe_allow_html=True)

# ====================================================================
# MODE 3: RESUME COMPARISON
# ====================================================================
elif app_mode == "⚖️ Resume Comparison":
    st.subheader("⚖️ Side-by-Side Resume Comparison (Old vs. New)")
    history_list = get_all_resumes()

    if len(history_list) < 2:
        st.info("💡 You need at least 2 uploaded resumes in history to compare. Upload more resumes in the Resume Analyzer tab!")
    else:
        cmp_col1, cmp_col2 = st.columns(2)
        with cmp_col1:
            id1 = st.selectbox("Select Resume 1 (Baseline)", [r["id"] for r in history_list], format_func=lambda x: f"ID {x}: {[r['name'] for r in history_list if r['id']==x][0]}")
        with cmp_col2:
            id2 = st.selectbox("Select Resume 2 (New)", [r["id"] for r in history_list], format_func=lambda x: f"ID {x}: {[r['name'] for r in history_list if r['id']==x][0]}")

        if id1 and id2:
            r1 = get_resume_by_id(id1)
            r2 = get_resume_by_id(id2)

            res_c1, res_c2 = st.columns(2)

            with res_c1:
                st.markdown(f"### 📄 {r1.get('name')}")
                st.metric("ATS Score", f"{r1.get('ats_score')} / 100")
                st.write(f"**Target Role:** {r1.get('target_role')}")
                st.write("**Skills:** " + ", ".join(r1.get("parsed_json", {}).get("skills_flat", [])))

            with res_c2:
                st.markdown(f"### 📄 {r2.get('name')}")
                diff = r2.get('ats_score', 0) - r1.get('ats_score', 0)
                st.metric("ATS Score", f"{r2.get('ats_score')} / 100", delta=f"{diff} pts")
                st.write(f"**Target Role:** {r2.get('target_role')}")
                st.write("**Skills:** " + ", ".join(r2.get("parsed_json", {}).get("skills_flat", [])))

# ====================================================================
# MODE 4: HISTORY & ANALYTICS
# ====================================================================
elif app_mode == "📜 History & Analytics":
    st.subheader("📜 Saved Resume History Dashboard (SQLite)")
    history_list = get_all_resumes()

    if history_list:
        df_hist = pd.DataFrame(history_list)
        st.dataframe(
            df_hist[["id", "name", "email", "ats_score", "strength", "target_role", "upload_date"]],
            use_container_width=True
        )

        st.markdown("---")
        del_id = st.number_input("Enter ID to Delete from History:", min_value=1, step=1)
        if st.button("🗑️ Delete Record"):
            delete_resume_record(int(del_id))
            st.success(f"Deleted record {del_id}. Please refresh!")
    else:
        st.info("No saved resumes in SQLite history database yet.")

# ====================================================================
# MODE 5: INTERVIEW PREP TIPS
# ====================================================================
elif app_mode == "💡 Interview Prep Tips":
    st.subheader("💡 Tailored Technical Interview Preparation Tips")
    
    skills_to_use = st.session_state.current_parsed.get("skills_flat", []) if st.session_state.current_parsed else ["python", "sql", "power bi", "machine learning"]
    tips_dict = get_interview_prep_tips(skills_to_use)

    for skill, tips in tips_dict.items():
        st.markdown(f"### 🧠 Interview Questions & Guidance for **{skill}**")
        for t in tips:
            st.write(f"• {t}")
        st.markdown("---")
