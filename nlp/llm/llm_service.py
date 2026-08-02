"""
==========================================================
LLM Service
==========================================================

Responsibilities
----------------
• Build prompt
• Call Mistral
• Parse response
"""

from llm.prompts import build_prompt
from llm.mistral import generate
from llm.parser import parse_response


async def generate_insights(
    context: dict
) -> dict:
    """
    Generate NLP insights.

    Parameters
    ----------
    context : dict

    Returns
    -------
    dict
    """

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    prompt = build_prompt(

        context

    )

    # --------------------------------------------------
    # Call Mistral
    # --------------------------------------------------

    llm_response = await generate(

        prompt

    )

    # --------------------------------------------------
    # Parse Response
    # --------------------------------------------------

    parsed_response = parse_response(

        llm_response

    )

    return parsed_response