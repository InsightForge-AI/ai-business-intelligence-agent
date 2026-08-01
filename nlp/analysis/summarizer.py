"""
==========================================================
Text Summarizer
==========================================================

Responsibilities
----------------
• Generate document summary
• Extract important sentences
"""

import re


def generate_summary(
    text: str,
    max_sentences: int = 3
) -> str:
    """
    Generate an extractive summary.

    Parameters
    ----------
    text : str

    max_sentences : int

    Returns
    -------
    str
    """

    if not text:

        return ""

    # -----------------------------------------------------
    # Split into Sentences
    # -----------------------------------------------------

    sentences = re.split(

        r'(?<=[.!?])\s+',

        text

    )

    sentences = [

        sentence.strip()

        for sentence in sentences

        if sentence.strip()

    ]

    if not sentences:

        return ""

    # -----------------------------------------------------
    # Return First N Sentences
    # -----------------------------------------------------

    summary = " ".join(

        sentences[:max_sentences]

    )

    return summary