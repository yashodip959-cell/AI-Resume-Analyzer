"""
SQLite Database Layer for AI Resume Analyzer History Dashboard
"""

import sqlite3
import os
import json
from datetime import datetime

DB_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(DB_DIR, "resume_history.db")

def get_connection():
    """Get SQLite database connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            ats_score INTEGER,
            strength TEXT,
            target_role TEXT,
            upload_date TEXT,
            parsed_json TEXT,
            pdf_path TEXT,
            txt_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_resume_record(parsed_data: dict, scoring_res: dict, target_role: str = "Data Analyst", pdf_path: str = "", txt_path: str = "") -> int:
    """Insert a processed resume record into SQLite database."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    name = parsed_data.get("name", "Unknown Candidate")
    email = parsed_data.get("email", "N/A")
    ats_score = scoring_res.get("total_score", 0)
    strength = scoring_res.get("strength", "N/A")
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parsed_json_str = json.dumps(parsed_data)

    cursor.execute("""
        INSERT INTO resume_history (name, email, ats_score, strength, target_role, upload_date, parsed_json, pdf_path, txt_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, ats_score, strength, target_role, upload_date, parsed_json_str, pdf_path, txt_path))

    record_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return record_id

def get_all_resumes() -> list:
    """Fetch all resume records sorted by upload date descending."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, ats_score, strength, target_role, upload_date, pdf_path, txt_path FROM resume_history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_resume_by_id(record_id: int) -> dict:
    """Fetch single resume record by ID."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resume_history WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        res = dict(row)
        res["parsed_json"] = json.loads(res["parsed_json"]) if res["parsed_json"] else {}
        return res
    return {}

def delete_resume_record(record_id: int) -> bool:
    """Delete a resume history record."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM resume_history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return True
