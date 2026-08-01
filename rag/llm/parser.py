"""
==========================================================
Qwen Response Parser
==========================================================

Responsibilities
----------------
• Parse JSON response
• Remove Markdown
• Remove thinking tags
• Extract JSON safely
• Validate output
"""

import json
import re


def parse_response(
    response: str
) -> dict:
    """
    Parse Qwen response safely.

    Parameters
    ----------
    response : str

    Returns
    -------
    dict
    """

    # -----------------------------------------------------
    # Empty Response
    # -----------------------------------------------------

    if not response:

        return {

            "answer": "I could not find the answer in the uploaded document.",

            "confidence": 0.0

        }

    # -----------------------------------------------------
    # Remove Markdown
    # -----------------------------------------------------

    response = re.sub(

        r"```json|```",

        "",

        response,

        flags=re.IGNORECASE

    ).strip()

    # -----------------------------------------------------
    # Remove Thinking Tags
    # -----------------------------------------------------

    response = re.sub(

        r"<think>.*?</think>",

        "",

        response,

        flags=re.DOTALL | re.IGNORECASE

    ).strip()

    # -----------------------------------------------------
    # Extract First JSON Object
    # -----------------------------------------------------

    match = re.search(

        r"\{.*\}",

        response,

        flags=re.DOTALL

    )

    if match:

        response = match.group(0)

    # -----------------------------------------------------
    # Parse JSON
    # -----------------------------------------------------

    try:

        parsed = json.loads(

            response

        )

    except Exception:

        return {

            "answer": response,

            "confidence": 0.50

        }

    # -----------------------------------------------------
    # Validate Answer
    # -----------------------------------------------------

    answer = parsed.get(

        "answer",

        "I could not find the answer in the uploaded document."

    )

    # -----------------------------------------------------
    # Validate Confidence
    # -----------------------------------------------------

    try:

        confidence = float(

            parsed.get(

                "confidence",

                0.90

            )

        )

    except Exception:

        confidence = 0.90

    confidence = max(

        0.0,

        min(

            confidence,

            1.0

        )

    )

    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return {

        "answer": answer,

        "confidence": confidence

    }