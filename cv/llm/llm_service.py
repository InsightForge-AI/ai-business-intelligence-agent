"""
==========================================================
LLM Service
==========================================================

Responsibilities
----------------
• Build prompt
• Call Llama
• Parse response
"""

from llm.prompts import build_prompt
from llm.llama import generate
from llm.parser import parse_response


async def generate_insights(
    context: dict
) -> dict:
    """
    Generate Computer Vision insights.

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
    # Call Llama
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