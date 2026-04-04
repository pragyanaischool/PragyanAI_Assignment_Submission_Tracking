# rag/document_loader.py

import os
from pypdf import PdfReader


# ==============================
# 📄 LOAD PDF
# ==============================

def load_pdf(file_path: str) -> str:
    """
    Load PDF and return LangChain documents
    """

    # Debug: check file existence
    print("📂 Checking file path:", file_path)
    print("📂 Absolute path:", os.path.abspath(file_path))

    if not os.path.exists(file_path):
        print("❌ File NOT FOUND:", file_path)
        return []

    print("✅ File FOUND:", file_path)

    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        print("📄 Loaded pages:", len(docs))

        if docs:
            print("🧠 Sample content:", docs[0].page_content[:200])

        return docs

    except Exception as e:
        print("❌ Error loading PDF:", str(e))
        return []

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
