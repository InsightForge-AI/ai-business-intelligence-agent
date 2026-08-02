"""
==========================================================
Vector Store
==========================================================

Responsibilities
----------------
• Store chunk embeddings
• Maintain in-memory vector index
• Preserve chunk metadata
"""

from typing import List, Dict

VECTOR_STORE: List[Dict] = []


def build_index(
    chunks: list,
    embeddings: list[list[float]]
):
    """
    Build in-memory vector index.

    Parameters
    ----------
    chunks : list
        List of chunk dictionaries.

    embeddings : list
        List of embedding vectors.
    """

    VECTOR_STORE.clear()

    for chunk, embedding in zip(chunks, embeddings):

        if not embedding:
            continue

        if isinstance(chunk, dict):

            VECTOR_STORE.append({

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

            VECTOR_STORE.append({

                "chunk_id": None,

                "text": str(chunk),

                "page": 1,

                "start_word": 0,

                "end_word": 0,

                "embedding": embedding

            })


def get_index() -> list:
    """
    Return vector index.
    """

    return VECTOR_STORE


def clear_index():
    """
    Clear vector store.
    """

    VECTOR_STORE.clear()


def index_size() -> int:
    """
    Return number of indexed chunks.
    """

    return len(VECTOR_STORE)