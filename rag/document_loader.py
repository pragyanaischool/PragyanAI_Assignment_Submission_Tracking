# rag/document_loader.py

import os
from pypdf import PdfReader


# ==============================
# 📄 LOAD PDF
# ==============================

def load_pdf(file_path: str) -> str:
    """Extract text from PDF"""
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        return text.strip()

    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")


# ==============================
# 📄 LOAD TEXT FILE
# ==============================

def load_txt(file_path: str) -> str:
    """Load plain text file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise ValueError(f"Error reading TXT: {str(e)}")


# ==============================
# 📄 LOAD DOCX
# ==============================

def load_docx(file_path: str) -> str:
    """Extract text from DOCX"""
    try:
        from docx import Document

        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

        return text.strip()

    except Exception as e:
        raise ValueError(f"Error reading DOCX: {str(e)}")


# ==============================
# 🚀 UNIVERSAL LOADER
# ==============================

def load_document(file_path: str) -> str:
    """
    Auto-detect file type and load content
    Supported: PDF, TXT, DOCX
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        return load_pdf(file_path)

    elif ext == "txt":
        return load_txt(file_path)

    elif ext == "docx":
        return load_docx(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
