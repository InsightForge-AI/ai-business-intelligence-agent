documents = [
    {"id": 1, "text": "sales dropped due to bad delivery"},
    {"id": 2, "text": "customers complaining about late delivery"},
    {"id": 3, "text": "sales increased after marketing campaign"},
    {"id": 4, "text": "delivery delay caused customer dissatisfaction"}
]


def simple_search(query: str):

    query_words = query.lower().split()
    results = []

    for doc in documents:
        text = doc["text"].lower()

        score = sum(1 for word in query_words if word in text)

        if score > 0:
            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results