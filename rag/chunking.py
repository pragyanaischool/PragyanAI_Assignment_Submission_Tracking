# rag/chunking.py

from typing import List
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


# ==============================
# 🧠 BASIC TEXT CHUNKING
# ==============================

def chunk_text(text: str) -> List[str]:
    """
    Split text into overlapping chunks
    """

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + CHUNK_SIZE

        chunk = text[start:end]
        chunks.append(chunk.strip())

        # Move with overlap
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ==============================
# 🧠 SMART CHUNKING (OPTIONAL)
# ==============================

def smart_chunk_text(text: str) -> List[str]:
    """
    Split text by paragraphs first, then merge intelligently
    """

    if not text:
        return []

    paragraphs = text.split("\n")

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()

        if not para:
            continue

        if len(current_chunk) + len(para) < CHUNK_SIZE:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ==============================
# 🔄 SELECT CHUNKING STRATEGY
# ==============================

def get_chunks(text: str, method: str = "default") -> List[str]:
    """
    method:
    - default → fixed chunk size
    - smart → paragraph-aware
    """

    if method == "smart":
        return smart_chunk_text(text)

    return chunk_text(text)
