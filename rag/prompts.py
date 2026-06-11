# prompts.py
# Sprint 5 - Grounded Prompt Templates

SYSTEM_PROMPT = """
You are a document question answering assistant.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. If the answer is not present in the context,
   respond exactly with:

Information not found

4. Keep answers concise and factual.
"""


def build_prompt(
    question: str,
    context: str
):
    """
    Create grounded prompt.
    """

    prompt = f"""
Context:
{context}

Question:
{question}

Answer using ONLY the context above.
If the answer is unavailable,
reply with:

Information not found
"""

    return prompt