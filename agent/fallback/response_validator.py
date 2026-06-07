VALID_MODULES = {"nlp", "ml", "cv", "rag"}


def validate_response(response: dict) -> bool:
    """
    Validate LLM routing output.
    """

    if not isinstance(response, dict):
        return False

    module = response.get("module")
    confidence = response.get("confidence")

    if module not in VALID_MODULES:
        return False

    if not isinstance(confidence, (int, float)):
        return False

    if confidence < 0 or confidence > 1:
        return False

    return True