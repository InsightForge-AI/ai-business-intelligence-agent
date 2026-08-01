"""
==========================================================
Re-Ranker
==========================================================

Responsibilities
----------------
• Improve retrieval order
• Rank chunks by semantic similarity
• Remove duplicate chunks
"""

from typing import List, Dict


def rerank_chunks(
    chunks: List[Dict]
) -> List[Dict]:
    """
    Re-rank retrieved chunks.

    Parameters
    ----------
    chunks : List[Dict]

    Returns
    -------
    List[Dict]
    """

    if not chunks:

        return []

    # -----------------------------------------------------
    # Remove duplicate chunks
    # -----------------------------------------------------

    unique_chunks = []

    seen = set()

    for chunk in chunks:

        chunk_id = chunk.get(

            "chunk_id"

        )

        if chunk_id in seen:

            continue

        seen.add(

            chunk_id

        )

        unique_chunks.append(

            chunk

        )

    # -----------------------------------------------------
    # Sort by similarity
    # -----------------------------------------------------

    unique_chunks.sort(

        key=lambda x: (

            x.get(

                "similarity",

                0.0

            ),

            len(

                x.get(

                    "text",

                    ""

                )

            )

        ),

        reverse=True

    )

    return unique_chunks