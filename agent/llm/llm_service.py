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

    intent = parse_response(

        llm_response

    )

    return intent