"""
==========================================================
Named Entity Recognition (NER)
==========================================================

Responsibilities
----------------
• Extract organizations
• Extract locations
• Extract people
• Extract years
• Extract percentages
• Extract monetary values
"""

import re

from utils.constants import MAX_ENTITIES


def extract_entities(
    text: str,
    max_entities: int = MAX_ENTITIES
) -> list[str]:
    """
    Extract named entities.

    Parameters
    ----------
    text : str

    max_entities : int

    Returns
    -------
    list[str]
    """

    if not text:

        return []

    entities = []

    # -----------------------------------------------------
    # Years
    # -----------------------------------------------------

    entities.extend(

        re.findall(

            r"\b(?:19|20)\d{2}\b",

            text

        )

    )

    # -----------------------------------------------------
    # Monetary Values
    # -----------------------------------------------------

    entities.extend(

        re.findall(

            r"[$€₹£]\s?\d+(?:,\d{3})*(?:\.\d+)?(?:\s?(?:million|billion|trillion))?",

            text,

            flags=re.IGNORECASE

        )

    )

    # -----------------------------------------------------
    # Percentages
    # -----------------------------------------------------

    entities.extend(

        re.findall(

            r"\b\d+(?:\.\d+)?%",

            text

        )

    )

    # -----------------------------------------------------
    # Multi-word Proper Nouns
    # Example:
    # ABC Corporation
    # Southeast Asia
    # New York
    # Artificial Intelligence
    # -----------------------------------------------------

    entities.extend(

        re.findall(

            r"\b(?:[A-Z][a-zA-Z&.-]*)(?:\s+[A-Z][a-zA-Z&.-]*)*\b",

            text

        )

    )

    # -----------------------------------------------------
    # Remove Noise
    # -----------------------------------------------------

    ignore = {

        "The",
        "A",
        "An",
        "This",
        "That",
        "These",
        "Those"

    }

    cleaned = []

    seen = set()

    for entity in entities:

        entity = entity.strip()

        if not entity:

            continue

        if entity in ignore:

            continue

        if entity in seen:

            continue

        seen.add(entity)

        cleaned.append(entity)

    return cleaned[:max_entities]