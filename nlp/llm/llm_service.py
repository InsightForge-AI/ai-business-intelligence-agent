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
        Empty on any failure (prompt/LLM/parse). nlp_service.py already
        reads every field via `llm.get(key, deterministic_fallback)`, so
        an empty dict here means callers transparently keep their own
        traditional-NLP results instead of the API raising a 500 --
        matching how ml/rag already degrade when their LLM is unavailable.
    """

    try:

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

        return parse_response(

            llm_response

        )

    except Exception:

        return {}