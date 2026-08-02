"""
==========================================================
Keyword Extraction
==========================================================

Responsibilities
----------------
• Extract important keywords
• Remove stop words
• Remove generic business words
• Support multi-word phrases
• Return top keywords
"""

import re
from collections import Counter

from utils.constants import MAX_KEYWORDS


STOP_WORDS = {

    "a", "an", "and", "are", "as", "at", "be", "by",
    "for", "from", "has", "have", "he", "in", "is",
    "it", "its", "of", "on", "that", "the", "to",
    "was", "were", "will", "with", "this", "these",
    "those", "their", "there", "or", "if", "into",
    "than", "then", "them", "they", "you", "your",
    "we", "our", "can", "may", "should", "would",
    "could", "not", "no", "yes"

}


GENERIC_WORDS = {

    "company",
    "business",
    "document",
    "report",
    "data",
    "information",
    "analysis",
    "using",
    "used",
    "performed",
    "performance",
    "improved",
    "increase",
    "decrease",
    "implemented",
    "resulted",
    "significant"

}


def extract_keywords(
    text: str,
    max_keywords: int = MAX_KEYWORDS
) -> list[str]:
    """
    Extract keywords from text.
    """

    if not text:

        return []

    # -----------------------------------------------------
    # Multi-word phrases
    # -----------------------------------------------------

    phrases = re.findall(

        r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b",

        text

    )

    # -----------------------------------------------------
    # Single words
    # -----------------------------------------------------

    words = re.findall(

        r"\b[a-zA-Z]{3,}\b",

        text.lower()

    )

    words = [

        word

        for word in words

        if word not in STOP_WORDS

        and word not in GENERIC_WORDS

    ]

    counter = Counter(words)

    keywords = []

    # -----------------------------------------------------
    # Add phrases first
    # -----------------------------------------------------

    for phrase in phrases:

        if phrase not in keywords:

            keywords.append(phrase)

    # -----------------------------------------------------
    # Add frequent words
    # -----------------------------------------------------

    for word, _ in counter.most_common():

        if len(keywords) >= max_keywords:

            break

        keyword = word.title()

        if keyword not in keywords:

            keywords.append(keyword)

    return keywords[:max_keywords]