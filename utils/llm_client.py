from groq import Groq
from config.settings import GROQ_API_KEY, LLM_MODEL, FAST_LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

def call_llm(prompt, fast=False):
    model = FAST_LLM_MODEL if fast else LLM_MODEL

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
