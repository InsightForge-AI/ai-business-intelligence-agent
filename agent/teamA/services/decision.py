# importing keywords for decision making
try:
    from ..config import ROUTING_KEYWORDS
except ImportError:
    from config import ROUTING_KEYWORDS

def decide(query: str) -> str:
    q = query.lower()
    for module, keywords in ROUTING_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            return module
    return "unknown"
