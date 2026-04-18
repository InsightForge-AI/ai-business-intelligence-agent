documents = [
    {"id": 1, "text": "sales dropped due to bad delivery"},
    {"id": 2, "text": "customers complaining about late delivery"},
    {"id": 3, "text": "sales increased after marketing campaign"},
    {"id": 4, "text": "delivery delay caused customer dissatisfaction"}
]


def simple_search(query: str):

    # Case 1 — empty query
    if not query or not query.strip():
        return []

    query_words = query.lower().split()

    results = []
    seen_ids = set()

    for doc in documents:

        text = doc["text"].lower()

        score = sum(1 for word in query_words if word in text)

        if score > 0:

            # Case 3 — remove duplicates
            if doc["id"] in seen_ids:
                continue

            seen_ids.add(doc["id"])

            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": score
            })

    # Case 4 — rank results (relevance)
    results.sort(key=lambda x: x["score"], reverse=True)

    return results