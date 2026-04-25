import re

# ---------------------------------------------------------------------------
# DATASET (keep simple but meaningful)
# ---------------------------------------------------------------------------
docs = [
    "sales dropped due to bad delivery",
    "customers complaining about late delivery",
    "delivery delay caused customer dissatisfaction",
    "revenue decreased last quarter",
    "shipping delays reported"
]

# ---------------------------------------------------------------------------
# SYNONYMS (semantic understanding)
# ---------------------------------------------------------------------------
SYNONYMS = {
    "late": ["delay", "delays"],
    "shipment": ["shipping", "delivery"],
    "delivery": ["shipping"],
    "complaint": ["complaints"],
    "issue": ["problem", "complaints", "delays"],
    "low": ["dropped", "decreased"],
    "sales": ["revenue"],
}

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
STOP_WORDS = {
    "the","a","an","is","it","in","on","at","to","for",
    "of","and","or","but","not","with","this","that"
}

MIN_SCORE = 3
MAX_RESULTS = 5

# ---------------------------------------------------------------------------
# CLEAN INPUT
# ---------------------------------------------------------------------------
def clean_query(query):
    if not isinstance(query, str):
        return ""
    query = query.lower()
    query = re.sub(r"[^a-z0-9\s]", "", query)
    query = re.sub(r"\s+", " ", query).strip()
    return query

# ---------------------------------------------------------------------------
# TOKENIZE
# ---------------------------------------------------------------------------
def tokenize(text):
    return [w for w in text.split() if w not in STOP_WORDS]

# ---------------------------------------------------------------------------
# EXPAND TOKENS (synonyms)
# ---------------------------------------------------------------------------
def expand(tokens):
    expanded = set(tokens)
    for t in tokens:
        if t in SYNONYMS:
            expanded.update(SYNONYMS[t])
    return list(expanded)

# ---------------------------------------------------------------------------
# SCORING (human-like relevance)
# ---------------------------------------------------------------------------
def score(doc, tokens):
    doc = doc.lower()
    score = 0

    match_count = 0

    for t in tokens:
        if t in doc:
            score += 2
            match_count += 1

    # bonus for multiple matches (important)
    if match_count >= 2:
        score += 2

    return score

# ---------------------------------------------------------------------------
# MAIN SEARCH FUNCTION
# ---------------------------------------------------------------------------
def search(query: str):

    # 1. Clean query
    query = clean_query(query)
    if not query:
        return {"content": [], "total_results": 0, "message": "empty query"}

    # 2. Tokenize
    tokens = tokenize(query)
    if not tokens:
        return {"content": [], "total_results": 0, "message": "empty query"}

    # 3. Expand (semantic)
    tokens = expand(tokens)

    # 4. Score documents
    scored = []
    for doc in docs:
        s = score(doc, tokens)
        if s >= MIN_SCORE:
            scored.append((s, doc))

    if not scored:
        return {"content": [], "total_results": 0, "message": "not found"}

    # 5. Sort + deduplicate
    scored.sort(key=lambda x: x[0], reverse=True)

    seen = set()
    results = []

    for _, doc in scored:
        if doc not in seen:
            seen.add(doc)
            results.append(doc)
        if len(results) >= MAX_RESULTS:
            break

    return {
        "query": query,
        "content": results,
        "total_results": len(results)
    }

# ---------------------------------------------------------------------------
# TEST BLOCK (add this)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_queries = [
        "delivery",
        "sales",
        "late shipment",
        "customer complaint",
        "low sales",
        "random text",
        "",
        "   ",
        "GOOD PRODUCT!!!",
        "good but late delivery",
        None,
        "customer complaints revenue",
    ]

    for q in test_queries:
        print(f"\nQuery: {repr(q)}")
        print(search(q))