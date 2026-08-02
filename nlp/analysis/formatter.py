"""
==========================================================
Analysis Formatter
==========================================================

Responsibilities
----------------
• Format NLP analysis results
• Build structured context
• Prepare data for the LLM
"""


def format_analysis(
    summary: str,
    keywords: list[str],
    entities: list[str],
    sentiment: str,
    topics: list[str],
    recommendations: list[str]
) -> dict:
    """
    Format NLP analysis.

    Parameters
    ----------
    summary : str

    keywords : list[str]

    entities : list[str]

    sentiment : str

    topics : list[str]

    recommendations : list[str]

    Returns
    -------
    dict
    """

    return {

        "summary": summary,

        "keywords": keywords,

        "entities": entities,

        "sentiment": sentiment,

        "topics": topics,

        "recommendations": recommendations

    }