"""
==========================================================
Document Chunker
==========================================================

Responsibilities
----------------
• Split document into semantic chunks
• Preserve paragraph context
• Support overlapping chunks
• Attach metadata for retrieval
"""

from utils.constants import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


def chunk_document(
    text: str
) -> list[dict]:
    """
    Split document into semantic chunks.

    Parameters
    ----------
    text : str

    Returns
    -------
    list[dict]
    """

    if not text or not text.strip():

        return []

    chunks = []

    chunk_id = 1

    paragraphs = [

        paragraph.strip()

        for paragraph in text.split("\n")

        if paragraph.strip()

    ]

    for paragraph in paragraphs:

        words = paragraph.split()

        # ---------------------------------------------
        # Small paragraph → keep as one chunk
        # ---------------------------------------------

        if len(words) <= CHUNK_SIZE:

            chunks.append({

                "chunk_id": chunk_id,

                "text": paragraph,

                "start_word": 0,

                "end_word": len(words),

                "page": 1

            })

            chunk_id += 1

            continue

        # ---------------------------------------------
        # Large paragraph → overlapping chunks
        # ---------------------------------------------

        start = 0

        while start < len(words):

            end = min(

                start + CHUNK_SIZE,

                len(words)

            )

            chunk_text = " ".join(

                words[start:end]

            )

            chunks.append({

                "chunk_id": chunk_id,

                "text": chunk_text,

                "start_word": start,

                "end_word": end,

                "page": 1

            })

            chunk_id += 1

            if end >= len(words):

                break

            start += (

                CHUNK_SIZE -

                CHUNK_OVERLAP

            )

    return chunks