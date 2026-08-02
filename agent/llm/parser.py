"""
==========================================================
Phi-3 Response Parser
==========================================================

Responsibilities
----------------
• Parse Phi-3 response
• Remove thinking tags
• Remove Markdown
• Extract JSON
• Validate intent
"""

import json
import re

from utils.constants import INTENTS


def parse_response(
    response: str
) -> str:
    """
    Parse Phi-3 response.

    Parameters
    ----------
    response : str

    Returns
    -------
    str
        Detected intent.
    """

    # --------------------------------------------------
    # Empty Response
    # --------------------------------------------------

    if not response:

        return "general_query"

    # --------------------------------------------------
    # Remove Thinking Tags
    # --------------------------------------------------

    response = re.sub(

        r"<think>.*?</think>",

        "",

        response,

        flags=re.DOTALL

    ).strip()

    # --------------------------------------------------
    # Remove Markdown
    # --------------------------------------------------

    response = response.replace(

        "```json",

        ""

    )

    response = response.replace(

        "```",

        ""

    ).strip()

    # --------------------------------------------------
    # Extract JSON
    # --------------------------------------------------

    match = re.search(

        r"\{.*\}",

        response,

        flags=re.DOTALL

    )

    if match:

        try:

            data = json.loads(

                match.group()

            )

            intent = data.get(

                "intent",

                "general_query"

            )

            if intent in INTENTS:

                return intent

        except Exception:

            pass

    # --------------------------------------------------
    # Plain Text Fallback
    # --------------------------------------------------

    response = response.strip()

    if response in INTENTS:

        return response

    # --------------------------------------------------
    # Default
    # --------------------------------------------------

    return "general_query"