# agents/hint_agent.py

from rag.prompt_templates import HINT_PROMPT, format_prompt
from utils.llm_client import call_llm


# ==============================
# 💡 GENERATE HINT
# ==============================

def generate_hint(question: str, context: str = "") -> str:
    """
    Generate a helpful hint for a given question using optional RAG context.

    Args:
        question (str): The question asked
        context (str): Retrieved context from RAG

    Returns:
        str: Hint text
    """

    try:
        # Build prompt
        prompt = format_prompt(
            HINT_PROMPT,
            question=question,
            context=context or "No additional context available"
        )

        # Call LLM (fast model for hints)
        response = call_llm(prompt, fast=True)

        return response.strip()

    except Exception as e:
        return f"⚠️ Unable to generate hint: {str(e)}"
