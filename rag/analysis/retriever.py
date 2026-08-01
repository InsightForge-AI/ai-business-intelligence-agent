"""
==========================================================
Retriever
==========================================================

Responsibilities
----------------
• Retrieve relevant chunks
• Perform cosine similarity search
• Return ranked chunk metadata
"""

from math import sqrt

from analysis.vector_store import get_index


def cosine_similarity(
    vector1: list[float],
    vector2: list[float]
) -> float:
    """
    Compute cosine similarity.
    """

    if not vector1 or not vector2:

        return 0.0

    dot = sum(

        a * b

        for a, b in zip(

            vector1,

            vector2

        )

    )

    norm1 = sqrt(

        sum(

            a * a

            for a in vector1

        )

    )

    norm2 = sqrt(

        sum(

            b * b

            for b in vector2

        )

    )

    if norm1 == 0 or norm2 == 0:

        return 0.0

    return dot / (

        norm1 * norm2

    )


def retrieve_chunks(
    query_embedding: list[float],
    top_k: int = 5
) -> list[dict]:
    """
    Retrieve most relevant chunks.

    Parameters
    ----------
    query_embedding : list[float]

    top_k : int

    Returns
    -------
    list[dict]
    """

    index = get_index()

    if not index:

        return []

    scored_chunks = []

    for item in index:

        embedding = item.get(

            "embedding",

            []

        )

        if not embedding:

            continue

        similarity = cosine_similarity(

            query_embedding,

            embedding

        )

        scored_chunks.append({

            "chunk_id": item.get(

                "chunk_id"

            ),

            "text": item.get(

                "text",

                ""

            ),

            "page": item.get(

                "page",

                1

            ),

            "start_word": item.get(

                "start_word",

                0

            ),

            "end_word": item.get(

                "end_word",

                0

            ),

            "similarity": similarity

        })

    scored_chunks.sort(

        key=lambda x: x["similarity"],

        reverse=True

    )

    return scored_chunks[:top_k]