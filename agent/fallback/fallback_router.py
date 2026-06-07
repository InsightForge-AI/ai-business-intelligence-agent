"""
Fallback Router

Used when:
1. LLM routing fails
2. LLM returns invalid module
3. Confidence is below threshold
"""

VALID_MODULES = {"nlp", "ml", "cv", "rag"}


def fallback_route(query: str, file_type: str = None) -> dict:
    """
    Rule-based fallback routing.

    Args:
        query (str): User query
        file_type (str): Detected file type

    Returns:
        dict: Routing decision
    """

    query = query.lower().strip()

    # -------------------------
    # File-based routing
    # -------------------------

    if file_type:
        file_type = file_type.lower()

        if file_type in ["csv", "xlsx", "xls"]:
            return {
                "module": "ml",
                "confidence": 0.90,
                "reason": "Structured data file detected"
            }

        if file_type in ["jpg", "jpeg", "png", "bmp"]:
            return {
                "module": "cv",
                "confidence": 0.90,
                "reason": "Image file detected"
            }

        if file_type == "pdf":
            return {
                "module": "rag",
                "confidence": 0.85,
                "reason": "PDF document detected"
            }

    # -------------------------
    # NLP Routing
    # -------------------------

    nlp_keywords = [
        "summary",
        "summarize",
        "rewrite",
        "translate",
        "paraphrase",
        "sentiment",
        "text"
    ]

    if any(keyword in query for keyword in nlp_keywords):
        return {
            "module": "nlp",
            "confidence": 0.75,
            "reason": "Text processing request detected"
        }

    # -------------------------
    # ML Routing
    # -------------------------

    ml_keywords = [
        "predict",
        "forecast",
        "sales",
        "trend",
        "analytics",
        "analysis",
        "classification",
        "regression"
    ]

    if any(keyword in query for keyword in ml_keywords):
        return {
            "module": "ml",
            "confidence": 0.75,
            "reason": "Analytics or prediction request detected"
        }

    # -------------------------
    # CV Routing
    # -------------------------

    cv_keywords = [
        "image",
        "photo",
        "object",
        "face",
        "detect",
        "vision"
    ]

    if any(keyword in query for keyword in cv_keywords):
        return {
            "module": "cv",
            "confidence": 0.75,
            "reason": "Computer vision request detected"
        }

    # -------------------------
    # RAG Routing
    # -------------------------

    rag_keywords = [
        "document",
        "pdf",
        "question",
        "answer",
        "report",
        "knowledge"
    ]

    if any(keyword in query for keyword in rag_keywords):
        return {
            "module": "rag",
            "confidence": 0.75,
            "reason": "Document question-answering request detected"
        }

    # -------------------------
    # Default Fallback
    # -------------------------

    return {
        "module": "rag",
        "confidence": 0.50,
        "reason": "No matching rule found; using default route"
    }