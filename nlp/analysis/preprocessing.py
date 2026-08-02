"""
==========================================================
Text Preprocessing
==========================================================

Responsibilities
----------------
• Normalize whitespace
• Remove extra newlines
• Remove tabs
"""

import re


def preprocess_text(
    text: str
) -> str:
    """
    Clean text.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """

    if not text:

        return ""

    # -----------------------------------------
    # Remove Tabs
    # -----------------------------------------

    text = text.replace(

        "\t",

        " "

    )

    # -----------------------------------------
    # Remove Multiple Newlines
    # -----------------------------------------

    text = re.sub(

        r"\n+",

        "\n",

        text

    )

    # -----------------------------------------
    # Normalize Spaces
    # -----------------------------------------

    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()