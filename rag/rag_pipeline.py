# rag/rag_pipeline.py
import streamlit as st
#from langchain.vectorstores import FAISS
#from langchain.embeddings import HuggingFaceEmbeddings
#from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from rag.document_loader import load_document
from rag.chunking import chunk_text
from rag.embeddings import get_embeddings
from rag.retriever import get_retriever

from groq import Groq
import os
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
    text = load_document(file_path)

    chunks = chunk_text(text)

    docs = [Document(page_content=c) for c in chunks]

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore


# ==============================
# 🔍 LOAD RAG PIPELINE
# ==============================
@st.cache_resource
def load_rag_pipeline(file_path):
    vectorstore = build_vector_store(file_path)
    retriever = get_retriever(vectorstore)

    return RAGPipeline(retriever)


# ==============================
# 🚀 RAG PIPELINE CLASS
# ==============================

class RAGPipeline:

    def __init__(self, retriever):
        self.retriever = retriever
        self.client = get_llm()

    def retrieve_context(self, query):
        docs = self.retriever.get_relevant_documents(query)
        return "\n".join([d.page_content for d in docs])

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def run(self, query):
        context = self.retrieve_context(query)

        prompt = f"""
        Use the context below to answer:

        Context:
        {context}

        Query:
        {query}
        """

        return self.generate(prompt)
