"""
==========================================================
LLM Service
==========================================================

Responsibilities
----------------
• Build prompt
• Call Qwen
• Parse response
• Handle LLM failures
"""

from llm.prompts import build_prompt
from llm.qwen import generate
from llm.parser import parse_response


async def generate_answer(
    context: dict
) -> dict:
    """
    Generate grounded answer using Qwen.

    Parameters
    ----------
    context : dict

    Returns
    -------
    dict
    """

    # --------------------------------------------------
    # Validate Context
    # --------------------------------------------------

    if not context:

        return {

            "answer": "No context available.",

            "confidence": 0.0

        }

    query = context.get(

        "query",

        ""

    )

    document_context = context.get(

        "context",

        ""

    )

    if not document_context:

        return {

            "answer": "I could not find any relevant information in the uploaded document.",

            "confidence": 0.0

        }

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    prompt = build_prompt(

        {

            "query": query,

            "context": document_context,

            "metadata": context.get(

                "metadata",

                {}

            )

        }

    )

    # --------------------------------------------------
    # Call Qwen
    # --------------------------------------------------

    try:

        llm_response = await generate(

            prompt

        )

    except Exception:

        return {

            "answer": "Unable to generate a response from the language model.",

            "confidence": 0.0

        }

    # --------------------------------------------------
    # Parse Response
    # --------------------------------------------------

    try:

        parsed_response = parse_response(

            llm_response

        )

    except Exception:

        return {

            "answer": "Unable to parse the model response.",

            "confidence": 0.0

        }

    # --------------------------------------------------
    # Ensure Standard Response
    # --------------------------------------------------

    return {

        "answer": parsed_response.get(

            "answer",

            "No answer generated."

        ),

        "confidence": float(

            parsed_response.get(

                "confidence",

                0.90

            )

        )

    }