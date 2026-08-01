"""
==========================================================
Topic Detection
==========================================================

Responsibilities
----------------
• Detect document topics
• Group important keywords
• Return major topics
"""

from utils.constants import MAX_TOPICS


TOPIC_MAPPING = {

    "Finance": {

        "revenue",
        "sales",
        "profit",
        "income",
        "expense",
        "cost",
        "budget",
        "financial",
        "margin"

    },

    "Business": {

        "customer",
        "market",
        "business",
        "strategy",
        "growth",
        "competition"

    },

    "Operations": {

        "production",
        "inventory",
        "logistics",
        "supply",
        "warehouse"

    },

    "Human Resources": {

        "employee",
        "staff",
        "recruitment",
        "training",
        "salary"

    },

    "Technology": {

        "software",
        "hardware",
        "cloud",
        "ai",
        "automation",
        "technology"

    }

}


def detect_topics(
    keywords: list[str]
) -> list[str]:
    """
    Detect document topics.

    Parameters
    ----------
    keywords : list[str]

    Returns
    -------
    list[str]
    """

    if not keywords:

        return []

    topics = []

    keyword_set = {

        keyword.lower()

        for keyword in keywords

    }

    for topic, vocabulary in TOPIC_MAPPING.items():

        if keyword_set.intersection(vocabulary):

            topics.append(topic)

    return topics[:MAX_TOPICS]