# rag/retriever.py

from config.settings import TOP_K_RETRIEVAL


# ==============================
# 🔍 DEFAULT RETRIEVER
# ==============================

def get_retriever(vectorstore):
    """
    Returns FAISS retriever with top-k results
    """
    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K_RETRIEVAL}
    )


# ==============================
# 🧠 CUSTOM RETRIEVAL FUNCTION
# ==============================

def retrieve_documents(vectorstore, query: str, k: int = None):
    """
    Manual retrieval (more control)
    """
    k = k or TOP_K_RETRIEVAL

    docs = vectorstore.similarity_search(query, k=k)

    return docs


# ==============================
# 🧠 FILTERED RETRIEVAL
# ==============================

def retrieve_with_filter(vectorstore, query: str, keyword: str = None):
    """
    Retrieve docs and filter by keyword
    """
    docs = vectorstore.similarity_search(query, k=TOP_K_RETRIEVAL)

    if keyword:
        docs = [d for d in docs if keyword.lower() in d.page_content.lower()]

    return docs


# ==============================
# 🧠 CONTEXT BUILDER
# ==============================

def build_context(docs):
    """
    Combine retrieved documents into single context
    """
    return "\n\n".join([doc.page_content for doc in docs])
