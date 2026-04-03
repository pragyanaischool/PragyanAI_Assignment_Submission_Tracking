# rag/embeddings.py

from langchain.embeddings import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL


# ==============================
# 🧠 LOAD EMBEDDING MODEL
# ==============================

def get_embeddings():
    """
    Returns embedding model
    Default: sentence-transformers
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


# ==============================
# 🔢 EMBED SINGLE TEXT
# ==============================

def embed_text(text: str):
    """
    Convert single text → vector
    """
    model = get_embeddings()
    return model.embed_query(text)


# ==============================
# 🔢 EMBED MULTIPLE TEXTS
# ==============================

def embed_documents(texts: list):
    """
    Convert list of texts → vectors
    """
    model = get_embeddings()
    return model.embed_documents(texts)
