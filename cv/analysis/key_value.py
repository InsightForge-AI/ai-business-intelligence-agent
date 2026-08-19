"""
==========================================================
Key-Value Extraction
==========================================================

Responsibilities
----------------
• Extract generic key-value pairs
• Normalize keys
• Remove duplicates
"""

import re


def extract_key_values(
    text: str
) -> dict:
    """
    Extract key-value pairs.

    Parameters
    ----------
    text : str

    Returns
    -------
    dict
    """

    if not text:

        return {}

    key_values = {}

    # -----------------------------------------------------
    # Match "Key : Value"
    # -----------------------------------------------------

    pattern = re.compile(

        r"^\s*([A-Za-z][A-Za-z0-9\s\/#().-]{1,50})\s*[:\-]\s*(.+)$",

        re.MULTILINE

    )

    matches = pattern.findall(

        text

    )

    for key, value in matches:

        key = (

            key.strip()

            .lower()

            .replace(

                " ",

                "_"

            )

        )

        value = value.strip()

        if value:

            key_values[key] = value

    return key_values