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
            "query": query,
            "content": [],
            "total_results": 0
        }

    # Handle very long query
    max_query_length = 500
    if len(query) > max_query_length:
        query = query[:max_query_length]

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["distances", "metadatas", "documents"]
    )

    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    documents = results.get("documents", [[]])[0]

    if not distances or not metadatas:
        return {
            "query": query,
            "content": [],
            "total_results": 0
        }

    # Filter low-quality matches
    threshold = 1.25
    valid_results = []
    for dist, meta, doc in zip(distances, metadatas, documents):
        if dist < threshold and meta and meta.get("answer"):
            valid_results.append((dist, meta.get("answer"), doc))

    if not valid_results:
        return {
            "query": query,
            "content": [],
            "total_results": 0
        }

    # Remove duplicates
    seen_answers = set()
    unique_results = []
    for dist, answer, doc in valid_results:
        if answer not in seen_answers:
            seen_answers.add(answer)
            unique_results.append((dist, answer, doc))

    # Sort by distance and limit to top_k
    unique_results.sort(key=lambda x: x[0])
    limited_results = unique_results[:top_k]

    # Format response
    content = [ans for _, ans, _ in limited_results]

    return {
        "query": query,
        "content": content,
        "total_results": len(content)
    }