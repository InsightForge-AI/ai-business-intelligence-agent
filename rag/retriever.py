# retriever.py
# Sprint 5 - RAG Retrieval Module
# Nandhitha + Narayani

import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

# ----------------------------------
# SAME MODEL AS ingest.py
# ----------------------------------

embedding_model = (
    SentenceTransformer(
        "all-MiniLM-L6-v2"
    )
)

# ----------------------------------
# CONFIG
# ----------------------------------

TOP_K = 5

MIN_SCORE = 0.50


# ----------------------------------
# QUERY EMBEDDING
# (Nandhitha)
# ----------------------------------

def embed_query(
    query: str
):

    embedding = (
        embedding_model.encode(
            [query],
            convert_to_numpy=True
        )
    )

    return embedding.astype(
        np.float32
    )


# ----------------------------------
# DISTANCE -> SCORE
# (Narayani)
# ----------------------------------

def normalize_score(
    distance
):
    """
    Convert FAISS L2 distance
    into confidence score.
    """

    score = 1 / (1 + distance)

    return round(
        float(score),
        4
    )


# ----------------------------------
# RETRIEVE CHUNKS
# (Nandhitha)
# ----------------------------------

def retrieve_chunks(
    query,
    index,
    chunks,
    top_k=TOP_K
):

    query_embedding = (
        embed_query(query)
    )

    distances, indices = (
        index.search(
            query_embedding,
            top_k
        )
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx == -1:
            continue

        score = (
            normalize_score(
                distance
            )
        )

        results.append(
            {
                "content": chunks[idx],
                "score": score,
                "distance": float(distance)
            }
        )

    return results


# ----------------------------------
# FILTER LOW QUALITY RESULTS
# (Narayani)
# ----------------------------------

def filter_chunks(
    retrieved_chunks,
    min_score=MIN_SCORE
):

    filtered = []

    for chunk in retrieved_chunks:

        if (
            chunk["score"]
            >= min_score
        ):

            filtered.append(
                chunk
            )

    filtered.sort(
        key=lambda x:
        x["score"],
        reverse=True
    )

    return filtered


# ----------------------------------
# BUILD CONTEXT
# ----------------------------------

def build_context(
    chunks
):

    context = "\n\n".join(
        [
            chunk["content"]
            for chunk in chunks
        ]
    )

    return context


# ----------------------------------
# MAIN RETRIEVER
# ----------------------------------

def retrieve_context(
    query,
    index,
    chunks,
    top_k=TOP_K
):

    retrieved = (
        retrieve_chunks(
            query,
            index,
            chunks,
            top_k
        )
    )

    filtered = (
        filter_chunks(
            retrieved
        )
    )

    context = (
        build_context(
            filtered
        )
    )

    return {
        "question": query,
        "retrieved_chunks":
            filtered,
        "context":
            context
    }


# ----------------------------------
# RETRIEVAL STATS
# (Narayani)
# ----------------------------------

def retrieval_statistics(
    chunks
):

    if len(chunks) == 0:

        return {
            "total_chunks": 0,
            "avg_score": 0
        }

    avg_score = sum(
        chunk["score"]
        for chunk in chunks
    ) / len(chunks)

    return {
        "total_chunks":
            len(chunks),
        "avg_score":
            round(avg_score, 4)
    }


# ----------------------------------
# TEST
# ----------------------------------

if __name__ == "__main__":

    from ingest import (
        build_document_index
    )

    sample_document = """
    Customers may request refunds
    within 7 days of purchase.

    Refunds require proof of purchase.

    Premium customers may receive
    priority processing.
    """

    index, chunks = (
        build_document_index(
            sample_document
        )
    )

    result = (
        retrieve_context(
            "What is refund policy?",
            index,
            chunks
        )
    )

    print("\nQUESTION:")
    print(
        result["question"]
    )

    print(
        "\nRETRIEVED CHUNKS:"
    )

    for chunk in (
        result[
            "retrieved_chunks"
        ]
    ):

        print("\n----------------")
        print(
            "Score:",
            chunk["score"]
        )
        print(
            chunk["content"]
        )

    stats = (
        retrieval_statistics(
            result[
                "retrieved_chunks"
            ]
        )
    )

    print(
        "\nSTATISTICS:"
    )
    print(stats)