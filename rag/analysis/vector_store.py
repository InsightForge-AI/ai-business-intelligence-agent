"""
==========================================================
Vector Store
==========================================================

Responsibilities
----------------
• Build an in-memory vector index for a single document's chunks
• Preserve chunk metadata

No AI logic.
"""

from typing import List, Dict


def build_index(
    chunks: list,
    embeddings: list[list[float]]
) -> List[Dict]:
    """
    Build an in-memory vector index for one document's chunks.

    Returns the index as a plain list -- it is NOT stored in any shared
    module-level state. An earlier version kept a single global
    VECTOR_STORE list that every call to build_index() cleared and
    replaced; under any concurrent usage (two documents processed by
    overlapping requests in the same process, which orchestration's
    `await generate_embeddings(...)` call makes reachable, not just
    theoretical) one document's retrieval could silently return another
    document's chunks. Callers (see services/rag_service.py) must now
    hold the returned index themselves and pass it to retrieve_chunks(),
    so each request's data stays request-scoped.

    Parameters
    ----------
    chunks : list
        List of chunk dictionaries.

    embeddings : list
        List of embedding vectors.

    Returns
    -------
    list[dict]
    """

    index: List[Dict] = []

    for chunk, embedding in zip(chunks, embeddings):

        if not embedding:
            continue

        if isinstance(chunk, dict):

            index.append({

                "chunk_id": chunk.get(
                    "chunk_id"
                ),

                "text": chunk.get(
                    "text",
                    ""
                ),

                "page": chunk.get(
                    "page",
                    1
                ),

                "start_word": chunk.get(
                    "start_word",
                    0
                ),

                "end_word": chunk.get(
                    "end_word",
                    0
                ),

                "embedding": embedding

            })

        else:

            index.append({

                "chunk_id": None,

                "text": str(chunk),

                "page": 1,

                "start_word": 0,

                "end_word": 0,

                "embedding": embedding

            })

    return index
