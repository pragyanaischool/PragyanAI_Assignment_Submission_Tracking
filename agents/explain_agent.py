# agents/explain_agent.py

from rag.prompt_templates import EXPLAIN_PROMPT, format_prompt
from groq import Groq
from config.settings import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def generate_explanation(question: str, context: str = ""):
    prompt = format_prompt(
        EXPLAIN_PROMPT,
        question=question,
        context=context
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
