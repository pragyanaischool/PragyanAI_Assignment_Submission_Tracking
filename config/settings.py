# config/settings.py

import os
from pathlib import Path
import streamlit as st

# ==============================

# 🔐 SECRETS (Streamlit First, Fallback to ENV)

# ==============================

def get_secret(key, default=None):
  try:
    return st.secrets[key]
  except Exception:
    return os.getenv(key, default)

GROQ_API_KEY = get_secret("GROQ_API_KEY")

# ==============================

# 📁 BASE PATHS

# ==============================

BASE_DIR = Path(**file**).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DOCS_DIR = DATA_DIR / "docs"
LOG_DIR = BASE_DIR / "logs"

for path in [DATA_DIR, UPLOAD_DIR, DOCS_DIR, LOG_DIR]:
os.makedirs(path, exist_ok=True)

# ==============================

# 📊 DATABASE FILES

# ==============================

USERS_FILE = DATA_DIR / "users.xlsx"
ASSIGNMENTS_FILE = DATA_DIR / "assignments.xlsx"
SUBMISSIONS_FILE = DATA_DIR / "submissions.xlsx"
TEST_SESSIONS_FILE = DATA_DIR / "test_sessions.xlsx"
QUESTION_LOGS_FILE = DATA_DIR / "question_logs.xlsx"

# ==============================

# 🤖 LLM CONFIG

# ==============================

LLM_MODEL = get_secret("LLM_MODEL", "llama-3.3-70b-versatile")
FAST_LLM_MODEL = get_secret("FAST_LLM_MODEL", "llama-3.3-70b-versatile")

LLM_TEMPERATURE = float(get_secret("LLM_TEMPERATURE", 0.3))
LLM_MAX_TOKENS = int(get_secret("LLM_MAX_TOKENS", 1024))

# ==============================

# 🧠 RAG CONFIG

# ==============================

EMBEDDING_MODEL = get_secret(
"EMBEDDING_MODEL",
"sentence-transformers/all-MiniLM-L6-v2"
)

CHUNK_SIZE = int(get_secret("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(get_secret("CHUNK_OVERLAP", 200))
TOP_K_RETRIEVAL = int(get_secret("TOP_K_RETRIEVAL", 3))

# ==============================

# 📝 TEST CONFIG

# ==============================

MAX_QUESTIONS = int(get_secret("MAX_QUESTIONS", 5))

ENABLE_HINTS = get_secret("ENABLE_HINTS", True)
ENABLE_EXPLANATION = get_secret("ENABLE_EXPLANATION", True)
ENABLE_EXAMPLES = get_secret("ENABLE_EXAMPLES", True)

# ==============================

# 👥 USER ROLES

# ==============================

ROLE_ADMIN = "admin"
ROLE_STUDENT = "student"

DEFAULT_ADMIN_ID = get_secret("DEFAULT_ADMIN_ID", "ADMIN01")
DEFAULT_ADMIN_PASSWORD = get_secret("DEFAULT_ADMIN_PASSWORD", "admin123")

# ==============================

# 📅 ASSIGNMENT SETTINGS

# ==============================

DEFAULT_DUE_DAYS = int(get_secret("DEFAULT_DUE_DAYS", 7))
ALLOW_LATE_SUBMISSION = get_secret("ALLOW_LATE_SUBMISSION", True)

# ==============================

# 📊 ANALYTICS CONFIG

# ==============================

ENABLE_ANALYTICS = get_secret("ENABLE_ANALYTICS", True)

TRACK_TIME_PER_QUESTION = get_secret("TRACK_TIME_PER_QUESTION", True)
TRACK_HINT_USAGE = get_secret("TRACK_HINT_USAGE", True)
TRACK_EXPLAIN_USAGE = get_secret("TRACK_EXPLAIN_USAGE", True)

# ==============================

# 📤 FILE UPLOAD CONFIG

# ==============================

MAX_FILE_SIZE_MB = int(get_secret("MAX_FILE_SIZE_MB", 10))
ALLOWED_FILE_TYPES = ["pdf", "docx", "txt", "png", "jpg"]

# ==============================

# ⚙️ PERFORMANCE

# ==============================

ENABLE_CACHE = get_secret("ENABLE_CACHE", True)
CACHE_TTL = int(get_secret("CACHE_TTL", 3600))

# ==============================

# 🔔 NOTIFICATIONS

# ==============================

ENABLE_DUE_ALERTS = get_secret("ENABLE_DUE_ALERTS", True)

# ==============================

# 🧾 LOGGING

# ==============================

LOG_FILE = LOG_DIR / "app.log"
LOG_LEVEL = get_secret("LOG_LEVEL", "INFO")

# ==============================

# 🚀 FUTURE FLAGS

# ==============================

USE_SQL_DB = get_secret("USE_SQL_DB", False)
USE_CLOUD_STORAGE = get_secret("USE_CLOUD_STORAGE", False)

# ==============================

# 🛠️ DEBUG

# ==============================

DEBUG = get_secret("DEBUG", True)
