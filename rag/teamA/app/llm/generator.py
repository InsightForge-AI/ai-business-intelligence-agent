import ollama

def generate_answer(query, docs):

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    You are a smart hospital assistant.

    Answer naturally and professionally using the context.

    If exact information is unavailable,
    give a helpful general response.

    Context:
    {context}

    User Question:
    {query}
    """

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]