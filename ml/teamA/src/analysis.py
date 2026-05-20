from .preprocess import preprocess
from .insights import get_insights


def analyze(query: str, call_llm) -> dict:
    """Run preprocessing and generate insights."""

    clean_query = preprocess(query)

    if not clean_query:
        return {
            "total_sales": None,
            "top_product": None,
            "trend": None,
            "error": "Empty or invalid query",
            "insights": None
        }

    return get_insights(clean_query, call_llm)