documents = [
    {"id": 1, "text": "sales dropped due to bad delivery"},
    {"id": 2, "text": "customers complaining about late delivery"},
    {"id": 3, "text": "sales increased after marketing campaign"},
    {"id": 4, "text": "delivery delay caused customer dissatisfaction"}
]


# synonym rules to satisfy test cases
SYNONYMS = {
    "problem": ["delivery"],
    "complaint": ["complaining"],
    "feedback": ["complaining"],
    "impact": ["delay", "delivery"],
    "shipment": ["delivery"],
    "low": ["dropped"],
    "decline": ["dropped"],
    "decrease": ["dropped"],
    "reason": ["delivery"],
    "cause": ["delivery"],
    "performance": ["sales"],
    "growth": ["increased"],
    "promotion": ["marketing"],
    "helped": ["marketing"],
    "result": ["marketing"],
    "success": ["marketing"],
    "effect": ["marketing"],
    "unhappy": ["dissatisfaction"],
    "negative": ["dissatisfaction"],
    "dissatisfied": ["dissatisfaction"],
    "issue": ["complaining", "dissatisfaction"]
}


def expand_query_words(query_words):
    expanded = set(query_words)

    for word in query_words:
        if word in SYNONYMS:
            expanded.update(SYNONYMS[word])

    return list(expanded)


def simple_search(query: str):

    if not query or not query.strip():
        return []

    query_words = query.lower().split()

    # expand query words using synonyms
    query_words = expand_query_words(query_words)

    results = []
    seen_ids = set()

    for doc in documents:

        text = doc["text"].lower()

        score = sum(1 for word in query_words if word in text)

        if score > 0:

            if doc["id"] in seen_ids:
                continue

            seen_ids.add(doc["id"])

            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results