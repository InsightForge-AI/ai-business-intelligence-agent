from rag.Team_C.vector_store.store import load_documents


def retrieve_documents(tokens):

    docs = load_documents()

    results = []

    for doc in docs:

        score = 0

        for token in tokens:

            if token in doc["text"]:
                score += 1

        if score > 0:

            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": score
            })

    return results