"""
==========================================================
Sentiment Analysis
==========================================================

Responsibilities
----------------
• Analyze document sentiment
• Classify as Positive, Neutral or Negative
"""

import re

from utils.constants import SENTIMENTS


POSITIVE_WORDS = {

    "good",
    "great",
    "excellent",
    "increase",
    "growth",
    "improved",
    "improvement",
    "profit",
    "success",
    "positive",
    "gain",
    "strong",
    "efficient",
    "benefit",
    "opportunity"

}


NEGATIVE_WORDS = {

    "bad",
    "poor",
    "loss",
    "decline",
    "decrease",
    "negative",
    "risk",
    "failure",
    "drop",
    "weak",
    "problem",
    "issue",
    "debt",
    "cost",
    "expense"

}


def analyze_sentiment(
    text: str
) -> str:
    """
    Analyze sentiment.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """

    if not text:

        return "Neutral"

    # -----------------------------------------
    # Tokenize
    # -----------------------------------------

    words = re.findall(

        r"\b\w+\b",

        text.lower()

    )

    positive = sum(

        1

        for word in words

        if word in POSITIVE_WORDS

    )

    negative = sum(

        1

        for word in words

        if word in NEGATIVE_WORDS

    )

    # -----------------------------------------
    # Classification
    # -----------------------------------------

    if positive > negative:

        return "Positive"

    if negative > positive:

        return "Negative"

    return "Neutral"