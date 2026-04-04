# rag/rag_pipeline.py

import streamlit as st
import os

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from rag.document_loader import load_document
from rag.chunking import chunk_text
from rag.embeddings import get_embeddings
from rag.retriever import get_retriever

from groq import Groq
from config.settings import GROQ_API_KEY


# ==============================
# 🤖 INIT LLM (GROQ)
# ==============================

def get_llm():
    return Groq(api_key=GROQ_API_KEY)


# ==============================
# 🧠 BUILD VECTOR STORE
# ==============================

def build_vector_store(file_path):

    print("📂 Checking file path:", file_path)
    print("📂 Absolute path:", os.path.abspath(file_path))
    print("📂 File exists:", os.path.exists(file_path))

    # Load document
    text = load_document(file_path)

    if not text:
        print("❌ No text extracted from document")
        return None

    # Chunk text
    chunks = chunk_text(text)

    if not chunks:
        print("❌ No chunks created")
        return None

    print("📄 Total chunks:", len(chunks))

    docs = [Document(page_content=c) for c in chunks]

    # Embeddings
    embeddings = get_embeddings()

    # Vector store
    vectorstore = FAISS.from_documents(docs, embeddings)

    print("✅ Vector store created")

    return vectorstore


# ==============================
# 🔍 LOAD RAG PIPELINE
# ==============================

@st.cache_resource
def load_rag_pipeline(file_path):

    vectorstore = build_vector_store(file_path)

    if vectorstore is None:
        print("❌ Using Dummy Retriever")
        return RAGPipeline(DummyRetriever())

    retriever = get_retriever(vectorstore)

    print("✅ Retriever ready")

    return RAGPipeline(retriever)


# ==============================
# 🚀 RAG PIPELINE CLASS
# ==============================

class RAGPipeline:

    def __init__(self, retriever):
        self.retriever = retriever
        self.client = get_llm()

    # ==============================
    # 🔍 RETRIEVE CONTEXT
    # ==============================
    def retrieve_context(self, query):
        try:
            docs = self.retriever.invoke(query)

            print("📚 Retrieved docs:", docs)

            if not docs:
                print("❌ No docs found")
                return ""

            context = "\n\n".join([
                doc.page_content for doc in docs
                if hasattr(doc, "page_content")
            ])

            return context

        except Exception as e:
            print("❌ Retriever Error:", str(e))
            return ""

    # ==============================
    # 🤖 GENERATE RESPONSE (LLM)
    # ==============================
    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    # ==============================
    # 🚀 MAIN RUN FUNCTION
    # ==============================
    def run(self, query):
        try:
            context = self.retrieve_context(query)

            if not context:
                return "⚠️ No content available from document."

            prompt = f"""
You are an AI tutor.

Use the context below to answer.

Context:
{context}

Question:
{query}

Give a clear and structured answer.
"""

            # ✅ FIXED (use generate instead of self.llm)
            return self.generate(prompt)

        except Exception as e:
            print("❌ RAG Error:", str(e))
            return "Error generating response"


# ==============================
# 🚨 FALLBACK RETRIEVER
# ==============================

class DummyRetriever:
    def invoke(self, query):
        return []
