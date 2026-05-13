from transformers import pipeline

# ----------------------------------
# LOAD QWEN MODEL
# ----------------------------------
generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B",
    device_map="auto"
)


def generate_llm_answer(query: str, results: list):

    if not results:
        return ""

    context = "\n".join(
        [r["text"] for r in results]
    )

    prompt = f"""
You are a grounded AI business assistant.

STRICT RULES:
1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. If answer is not found in context,
   reply exactly:
   "Information not available in retrieved documents."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    try:

        output = generator(
            prompt,
            max_new_tokens=80,
            do_sample=False
        )

        generated_text = output[0]["generated_text"]

        answer = generated_text.split("ANSWER:")[-1].strip()

        if len(answer) < 3:
            return "Information not available in retrieved documents."

        return answer

    except Exception:

        return "LLM generation failed."