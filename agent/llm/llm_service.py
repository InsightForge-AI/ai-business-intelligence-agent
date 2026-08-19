"""
==========================================================
LLM Service
==========================================================

Responsibilities
----------------
• Build Phi-3 prompt
• Call Phi-3
• Parse response
• Return detected intent
"""

from llm.prompts import build_prompt
from llm.phi3 import generate
from llm.parser import parse_response


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

    # Any failure here (prompt build, Phi-3 call, or parsing) returns ""
    # rather than raising -- routing/intent_detector.py already has
    # `if not intent: return "general_query"`, a fallback written for
    # an empty LLM response that this reuses for a failed one too,
    # instead of the API raising a 500.
    try:

        # --------------------------------------------------
        # Build Prompt
        # --------------------------------------------------

        prompt = build_prompt(

            query=query,

            metadata=metadata

        )

        # --------------------------------------------------
        # Phi-3
        # --------------------------------------------------

        llm_response = await generate(

            prompt

        )

        # --------------------------------------------------
        # Parse Response
        # --------------------------------------------------

        return parse_response(

            llm_response

        )

    except Exception:

        return ""