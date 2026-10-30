"""
Interactive Plotly Chart Generators for Streamlit Dashboard
Generates ATS Gauge, Skill Donut, Score Breakdown Bar, and Radar charts.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

def create_ats_gauge_chart(score: float) -> go.Figure:
    """Create radial gauge chart for ATS Score (0 - 100)."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>ATS Score</b>", 'font': {'size': 22, 'color': '#6C5CE7'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#4A5568"},
            'bar': {'color': "#6C5CE7", 'thickness': 0.3},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#2D3748",
            'steps': [
                {'range': [0, 50], 'color': '#FF7675'},
                {'range': [50, 75], 'color': '#FFEAA7'},
                {'range': [75, 100], 'color': '#55E6C1'}
            ],
            'threshold': {
                'line': {'color': "#A29BFE", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#E2E8F0", 'family': "Inter, sans-serif"},
        margin=dict(l=20, r=20, t=50, b=20),
        height=280
    )
    return fig

def create_skill_donut_chart(categorized_skills: dict) -> go.Figure:
    """Create Skill Category Distribution Donut Chart."""
    categories = []
    counts = []

    for cat, skills in categorized_skills.items():
        categories.append(cat)
        counts.append(len(skills))

    if not categories:
        categories = ["No Skills Found"]
        counts = [1]

    fig = px.pie(
        names=categories,
        values=counts,
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Purples_r,
        title="<b>Skill Distribution by Category</b>"
    )

    fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#1A202C', width=2)))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#E2E8F0"},
        margin=dict(l=10, r=10, t=40, b=10),
        height=280
    )
    return fig

def create_score_breakdown_bar(breakdown: dict) -> go.Figure:
    """Horizontal bar chart showing score breakdown against maximum points."""
    categories = list(breakdown.keys())
    scores = [v["score"] for v in breakdown.values()]
    max_scores = [v["max"] for v in breakdown.values()]

    df = pd.DataFrame({
        "Category": categories,
        "Score": scores,
        "Max Score": max_scores
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df["Category"],
        x=df["Max Score"],
        name="Max Points",
        orientation='h',
        marker=dict(color='#2D3748')
    ))

    fig.add_trace(go.Bar(
        y=df["Category"],
        x=df["Score"],
        name="Earned Points",
        orientation='h',
        marker=dict(color='#6C5CE7')
    ))

    fig.update_layout(
        barmode='overlay',
        title="<b>ATS Score Category Breakdown</b>",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#E2E8F0"},
        xaxis=dict(showgrid=True, gridcolor="#2D3748"),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=300
    )
    return fig

def create_skill_radar_chart(user_skills_flat: list) -> go.Figure:
    """Create Skill Readiness Radar Chart across 5 key pillars."""
    user_set = set([s.lower() for s in user_skills_flat])

    pillars = {
        "Programming": ["python", "java", "c++", "javascript", "sql"],
        "Data Analysis": ["excel", "power bi", "tableau", "pandas", "statistics"],
        "Databases & Cloud": ["mysql", "postgresql", "mongodb", "aws", "docker"],
        "Web & Frameworks": ["html", "css", "react", "django", "flask"],
        "ML & AI": ["machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn"]
    }

    scores = []
    labels = list(pillars.keys())

    for pillar, skill_list in pillars.items():
        matches = sum(1 for s in skill_list if s in user_set)
        score = (matches / len(skill_list)) * 100
        scores.append(round(score, 1))

    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=labels,
        fill='toself',
        fillcolor='rgba(108, 92, 231, 0.4)',
        line=dict(color='#A29BFE', width=2)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#A0AEC0", gridcolor="#2D3748"),
            angularaxis=dict(color="#E2E8F0")
        ),
        showlegend=False,
        title="<b>Technical Skills Radar Map</b>",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#E2E8F0"},
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return fig
