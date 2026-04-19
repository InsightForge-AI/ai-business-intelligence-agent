# This module is done by Rana Kumar and Chandrashekar

import chromadb

def create_collection(docs, embeddings, metadatas):
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="rag_collection")

    ids = [str(i) for i in range(len(docs))]

    collection.add(
        documents=docs,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    return collection


def search(query, model, collection, top_k=3):
    if not query or not query.strip():
        return {
            "context": "no query provided",
            "source": None,
            "error": None
        }

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=1,
        include=["distances", "metadatas"]
    )

    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not distances or not metadatas:
        return {
            "context": "no data found",
            "source": None,
            "error": None
        }

    best_distance = distances[0]
    answer = metadatas[0].get("answer") if isinstance(metadatas[0], dict) else None

    # Threshold chosen from observed distances: related FAQ answers are around ~1.08-1.22,
    # unrelated queries like "weather today" were around ~1.28.
    if best_distance >= 1.25 or not answer:
        return {
            "context": "out of context",
            "source": None,
            "error": None
        }

    return {
        "context": answer,
        "source": "faq.txt",
        "error": None
    }