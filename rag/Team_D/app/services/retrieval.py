# This module is done by Rana Kumar

import chromadb

def create_collection(docs, embeddings):
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="rag_collection")

    ids = [str(i) for i in range(len(docs))]

    collection.add(
        documents=docs,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    return collection


def search(query, model, collection, top_k=3):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0]