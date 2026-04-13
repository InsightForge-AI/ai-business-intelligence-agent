from ..config import ROUTING_KEYWORDS

def decide(query: str) -> str:
    q = query.lower()
    for module, keywords in ROUTING_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            return module
    return "unknown"
