from ..config import ROUTING_KEYWORDS


def decide(query: str) -> str:
    """
    Decide which module should handle the query.
    Handles multiple intents, ambiguous queries, and unknown queries.
    """

    if not query or not query.strip():
        return "unknown"

    q = query.lower()

    detected_modules = []

    # detect modules based on keywords
    for module, keywords in ROUTING_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            detected_modules.append(module)

    # remove duplicates
    detected_modules = list(set(detected_modules))

    # Case 1: No module detected
    if not detected_modules:
        return "unknown"

    # Case 2: Multiple modules detected
    # For Sprint-3 stability, prioritize modules
    priority_order = ["ml", "nlp", "rag", "cv"]

    for module in priority_order:
        if module in detected_modules:
            return module

    # fallback
    return "unknown"