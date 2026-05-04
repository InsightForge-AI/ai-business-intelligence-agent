def preprocess(query: str) -> str:
    """Clean and validate the user query before sending to LLM."""
    if not query or not query.strip():
        return None
    query = " ".join(query.strip().split())
    return query