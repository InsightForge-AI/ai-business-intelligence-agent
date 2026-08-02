"""
==========================================================
Context Formatter
==========================================================

Responsibilities
----------------
• Prepare retrieved context
• Preserve page information
• Build clean prompt context
"""

from typing import List, Dict


def format_context(
    chunks: List[Dict]
) -> str:
    """
    Format retrieved chunks into readable context.

    Parameters
    ----------
    chunks : List[Dict]

    Returns
    -------
    str
    """

    if not chunks:

        return ""

    context = []

    for chunk in chunks:

        page = chunk.get(

            "page",

            1

        )

        chunk_id = chunk.get(

            "chunk_id",

            "?"

        )

        similarity = chunk.get(

            "similarity",

            0.0

        )

        text = chunk.get(

            "text",

            ""

        ).strip()

        if not text:

            continue

        context.append(

            f"""
==================================================
Page: {page}
Chunk: {chunk_id}
Similarity: {similarity:.3f}
==================================================

{text}
""".strip()

        )

    return "\n\n".join(

        context

    )