"""
routing/query_router.py
-----------------------
Rule-based, multi-module query router (the deterministic "brain").

This is the heart of the rule layer. It looks at:
  1. keyword signals in the question, and
  2. the uploaded file's type,
then returns the set of modules that should handle the request.

It also exposes which signals fired so the confidence layer can score the
decision. Designed to be the safe fallback whenever LLM routing is
unavailable or returns something invalid.

"""

from routing.keyword_rules import KEYWORDS
from utils.constants import (
    DEFAULT_MODULE,
    DOCUMENT_EXTS,
    IMAGE_EXTS,
    STRUCTURED_EXTS,
)
from utils.helpers import normalize_text


def route_query(question: str, file_type: str = None) -> list:
    """
    Return the list of modules for a query (backward-compatible signature).

    Args:
        question:  the user's question / instruction
        file_type: file extension including the dot, e.g. ".csv" (optional)

    Returns:
        sorted list[str] of module names, e.g. ["nlp", "rag"]
    """
    decision = route_query_detailed(question, file_type)
    return decision["modules"]


def route_query_detailed(question: str, file_type: str = None) -> dict:
    """
    Same routing logic as route_query, but also returns the signals that
    fired so other layers can compute confidence and reasons.

    Returns a dict:
        {
            "modules": [...],
            "keyword_hit": bool,   # at least one keyword matched
            "file_hit": bool,      # the file type drove a decision
            "is_default": bool,    # nothing matched -> default used
        }
    """
    modules = set()
    keyword_hit = False
    file_hit = False

    q = normalize_text(question)
    ext = (file_type or "").lower().strip()

    # ------------------------------------------------------------------ #
    # 1. Keyword-based routing
    # ------------------------------------------------------------------ #
    if q:
        for module, keywords in KEYWORDS.items():
            if any(kw in q for kw in keywords):
                modules.add(module)
                keyword_hit = True

    # ------------------------------------------------------------------ #
    # 2. File-type based routing
    # ------------------------------------------------------------------ #
    if ext:
        if ext in STRUCTURED_EXTS:
            modules.add("ml")
            file_hit = True
        elif ext in IMAGE_EXTS:
            modules.add("cv")
            file_hit = True
        elif ext in DOCUMENT_EXTS:
            modules.add("rag")
            file_hit = True

    # ------------------------------------------------------------------ #
    # 3. Smart multi-module combinations
    # ------------------------------------------------------------------ #
    summary_words = ("summarize", "summarise", "summary", "overview")

    # A document that also needs summarizing -> RAG + NLP
    if ext in DOCUMENT_EXTS and any(w in q for w in summary_words):
        modules.update({"rag", "nlp"})

    # An image that also needs text understanding -> CV + NLP
    if ext in IMAGE_EXTS and any(
        w in q for w in ("summarize", "summarise", "extract", "text", "read")
    ):
        modules.update({"cv", "nlp"})

    # ------------------------------------------------------------------ #
    # 4. Default route — never return an empty decision
    # ------------------------------------------------------------------ #
    is_default = False
    if not modules:
        modules.add(DEFAULT_MODULE)
        is_default = True

    return {
        "modules": sorted(modules),
        "keyword_hit": keyword_hit,
        "file_hit": file_hit,
        "is_default": is_default,
    }


# Quick manual check (run from agent/):  python -m routing.query_router
if __name__ == "__main__":
    samples = [
        ("Summarize this report", None),
        ("Which region has low sales?", ".xlsx"),
        ("What is shown in this image?", ".png"),
        ("Answer questions from this PDF", ".pdf"),
        ("Summarize this PDF report", ".pdf"),
        ("Extract text from image and summarize", ".jpg"),
    ]
    for question, ftype in samples:
        print(f"{question!r:55} {ftype}  ->  {route_query(question, ftype)}")
