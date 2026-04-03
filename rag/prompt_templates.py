# rag/prompt_templates.py

# ==============================
# 🧠 QUESTION GENERATION
# ==============================

QUESTION_PROMPT = """
You are an expert educator.

Based on the following context, generate {num_questions} conceptual questions.

Rules:
- Do NOT provide answers
- Focus on understanding and application
- Keep questions clear and concise

Context:
{context}
"""


# ==============================
# 💡 HINT GENERATION
# ==============================

HINT_PROMPT = """
You are a helpful tutor.

Provide a hint for the question below.

Rules:
- Do NOT give the final answer
- Guide thinking process
- Keep it short

Question:
{question}

Context:
{context}
"""


# ==============================
# 🧠 EXPLANATION PROMPT
# ==============================

EXPLAIN_PROMPT = """
You are an expert teacher.

Explain the concept behind the question in a clear and simple way.

Rules:
- Step-by-step explanation
- Beginner friendly
- Use examples if needed

Question:
{question}

Context:
{context}
"""


# ==============================
# 📘 EXAMPLE PROMPT
# ==============================

EXAMPLE_PROMPT = """
You are a tutor.

Provide a similar example problem with solution to help understand the concept.

Rules:
- Similar difficulty
- Include solution
- Keep it simple

Question:
{question}

Context:
{context}
"""


# ==============================
# 🔍 RAG ANSWERING PROMPT
# ==============================

RAG_PROMPT = """
Answer the question using ONLY the provided context.

Rules:
- Do not hallucinate
- If answer not in context, say "Not found in document"
- Be clear and concise

Context:
{context}

Question:
{question}
"""


# ==============================
# 📊 ANALYTICS INSIGHT PROMPT
# ==============================

ANALYTICS_PROMPT = """
You are an AI learning analyst.

Analyze the student's performance data and provide insights.

Focus on:
- Strengths
- Weaknesses
- Recommendations

Data:
{data}
"""


# ==============================
# 🧠 FORMATTER FUNCTIONS
# ==============================

def format_prompt(template: str, **kwargs):
    """
    Replace placeholders in prompt
    """
    return template.format(**kwargs)
