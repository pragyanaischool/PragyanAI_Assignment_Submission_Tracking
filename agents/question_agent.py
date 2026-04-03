# agents/question_agent.py

from rag.prompt_templates import QUESTION_PROMPT, format_prompt
from config.settings import MAX_QUESTIONS
from groq import Groq
from config.settings import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)


def generate_questions(context: str, num_questions: int = MAX_QUESTIONS):
    prompt = format_prompt(
        QUESTION_PROMPT,
        context=context,
        num_questions=num_questions
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
