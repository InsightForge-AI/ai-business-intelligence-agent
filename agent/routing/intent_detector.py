"""
==========================================================
Intent Detector
==========================================================

Responsibilities
----------------
• Detect user intent
• Use Phi-3 through the LLM service
• Return the detected intent
"""

from llm.llm_service import detect_intent as llm_detect_intent


async def detect_intent(
    query: str,
    metadata: dict
) -> str:
    """
    Detect the user's intent.

    Parameters
    ----------
    query : str

    metadata : dict

    Returns
    -------
    str
    """

    # -----------------------------------------
    # Detect Intent Using Phi-3
    # -----------------------------------------

    intent = await llm_detect_intent(

        query=query,

        metadata=metadata

    )

    # -----------------------------------------
    # Fallback
    # -----------------------------------------

    if not intent:

        return "general_query"

    return intent