from typing import Optional


def preprocess(query: str) -> Optional[str]:
    """Clean and validate the user query before sending to LLM."""

    if not query or not query.strip():
        return None

    return " ".join(query.strip().split())