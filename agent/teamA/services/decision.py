from ..config import ROUTING_KEYWORDS


def decide(query: str) -> str:
    if not query or not query.strip():
        return "unknown"

    q = query.lower()

    detected_modules = []

    for module, keywords in ROUTING_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            detected_modules.append(module)

    detected_modules = list(set(detected_modules))

    # no module detected
    if not detected_modules:
        return "unknown"

    # multiple modules detected → ambiguous
    if len(detected_modules) > 1:
        return "nlp"

    # single module
    return detected_modules[0]