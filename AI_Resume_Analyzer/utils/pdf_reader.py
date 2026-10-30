"""
PDF and DOCX Document Reader Utility
Handles text extraction from resume files cleanly.
"""

import io
import PyPDF2
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

def extract_text_from_pdf(file_bytes_or_path) -> str:
    """Extract raw text from a PDF file (bytes or file path) using pdfplumber/PyPDF2."""
    text = ""
    
    # Try pdfplumber first for accurate layout & text extraction
    if HAS_PDFPLUMBER:
        try:
            if isinstance(file_bytes_or_path, (str, bytes)):
                file_obj = io.BytesIO(file_bytes_or_path) if isinstance(file_bytes_or_path, bytes) else file_bytes_or_path
            else:
                file_obj = file_bytes_or_path

            with pdfplumber.open(file_obj) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text.strip()
        except Exception:
            pass

    # Fallback to PyPDF2
    try:
        if isinstance(file_bytes_or_path, bytes):
            file_obj = io.BytesIO(file_bytes_or_path)
        elif isinstance(file_bytes_or_path, str):
            file_obj = open(file_bytes_or_path, 'rb')
        else:
            file_obj = file_bytes_or_path

        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text.strip()

def extract_text_from_docx(file_bytes_or_path) -> str:
    """Extract raw text from a DOCX file."""
    if not HAS_DOCX:
        return ""
    try:
        if isinstance(file_bytes_or_path, bytes):
            file_obj = io.BytesIO(file_bytes_or_path)
        else:
            file_obj = file_bytes_or_path
            
        doc = docx.Document(file_obj)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def extract_resume_text(uploaded_file) -> str:
    """Main router to extract text from Streamlit UploadedFile or file path."""
    if uploaded_file is None:
        return ""

    if isinstance(uploaded_file, str):
        if uploaded_file.endswith('.pdf'):
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.endswith('.docx'):
            return extract_text_from_docx(uploaded_file)
        return ""

    filename = getattr(uploaded_file, 'name', '').lower()
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0) # reset position

    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    else:
        # try as PDF
        return extract_text_from_pdf(file_bytes)
