"""
Comprehensive Skills & Job Role Database for AI Resume Analyzer
"""

SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "r", "go", 
        "rust", "kotlin", "swift", "php", "ruby", "scala", "sql", "bash", "shell"
    ],
    "Data & AI / ML": [
        "machine learning", "deep learning", "data science", "pandas", "numpy", 
        "scikit-learn", "tensorflow", "pytorch", "keras", "nlp", "computer vision", 
        "spacy", "nltk", "opencv", "power bi", "tableau", "excel", "matplotlib", 
        "seaborn", "plotly", "spark", "hadoop", "bigquery", "snowflake", "data analysis",
        "data engineering", "predictive modeling", "statistics", "data mining"
    ],
    "Web & Frameworks": [
        "html", "css", "react", "angular", "vue", "next.js", "node.js", "express", 
        "django", "flask", "fastapi", "spring boot", "bootstrap", "tailwind", 
        "rest api", "graphql", "streamlit"
    ],
    "Databases": [
        "mysql", "postgresql", "sqlite", "mongodb", "redis", "oracle", "sql server", 
        "dynamodb", "cassandra", "elasticsearch"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "gitlab", 
        "jenkins", "terraform", "ansible", "ci/cd", "linux", "bash", "cloud computing"
    ],
    "Soft Skills & Leadership": [
        "communication", "problem solving", "critical thinking", "teamwork", 
        "leadership", "time management", "project management", "agile", "scrum", 
        "collaboration", "adaptability", "analytical skills", "creativity"
    ]
}

# Target Job Benchmark Skills
JOB_BENCHMARKS = {
    "Data Analyst": {
        "required_skills": ["python", "sql", "excel", "power bi", "tableau", "statistics", "data analysis"],
        "good_to_have": ["r", "pandas", "numpy", "bigquery", "communication"],
        "description": "Analyzes complex data sets to provide business insights."
    },
    "Data Scientist": {
        "required_skills": ["python", "machine learning", "sql", "pandas", "scikit-learn", "statistics", "data science"],
        "good_to_have": ["deep learning", "tensorflow", "pytorch", "power bi", "bigquery", "r"],
        "description": "Builds predictive models and machine learning algorithms."
    },
    "BI Developer": {
        "required_skills": ["power bi", "tableau", "sql", "data modeling", "excel", "dax"],
        "good_to_have": ["python", "ssis", "ssrs", "etl", "snowflake"],
        "description": "Designs and develops business intelligence reporting solutions."
    },
    "Python Developer": {
        "required_skills": ["python", "django", "flask", "fastapi", "sql", "git", "rest api"],
        "good_to_have": ["docker", "postgresql", "redis", "celery", "aws", "pytest"],
        "description": "Develops backend applications and automation scripts using Python."
    },
    "Full Stack Developer": {
        "required_skills": ["javascript", "react", "node.js", "html", "css", "sql", "git", "rest api"],
        "good_to_have": ["typescript", "next.js", "mongodb", "docker", "aws", "tailwind"],
        "description": "Builds client-side and server-side web applications."
    },
    "Business Analyst": {
        "required_skills": ["excel", "sql", "power bi", "project management", "agile", "documentation", "analytical skills"],
        "good_to_have": ["python", "tableau", "scrum", "jira", "communication"],
        "description": "Bridges the gap between IT and business teams using data driven insights."
    },
    "AI / Machine Learning Engineer": {
        "required_skills": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn", "docker"],
        "good_to_have": ["nlp", "computer vision", "fastapi", "mlops", "gcp", "aws"],
        "description": "Deploys scalable machine learning models into production systems."
    }
}

INTERVIEW_TIPS = {
    "python": [
        "Be ready to explain Python List Comprehensions vs Generators.",
        "Practice GIL (Global Interpreter Lock) and multi-threading concepts.",
        "Expect questions on decorators, dunder methods, and memory management."
    ],
    "sql": [
        "Practice writing complex JOINs, GROUP BY, and HAVING queries.",
        "Understand Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG).",
        "Be prepared to explain indexing, query optimization, and transaction isolation."
    ],
    "power bi": [
        "Explain the difference between Calculated Columns and Measures in DAX.",
        "Practice explaining Star Schema vs Snowflake Schema data modeling.",
        "Be ready to discuss Row Level Security (RLS) implementation."
    ],
    "machine learning": [
        "Explain Bias-Variance tradeoff and techniques to prevent overfitting.",
        "Be ready to explain metrics: Precision, Recall, F1-Score, ROC-AUC.",
        "Understand tree-based models (Random Forest, XGBoost) vs Linear Models."
    ],
    "react": [
        "Explain React Virtual DOM and reconciliation process.",
        "Be ready to discuss React Hooks (useEffect, useMemo, useCallback).",
        "Understand State Management patterns (Context API, Redux Toolkit)."
    ]
}
