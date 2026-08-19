"""
==========================================================
Mistral Response Parser
==========================================================

Responsibilities
----------------
• Parse Mistral response
• Remove thinking tags
• Remove Markdown
• Extract JSON
• Normalize response
"""

import json
import re


def normalize_list(items):
    """
    Convert LLM output into List[str].
    """

    if not isinstance(items, list):

        return []

    result = []

    for item in items:

        if isinstance(item, str):

            item = item.strip()

            if item:

                result.append(item)

        elif isinstance(item, dict):

            value = " ".join(

                str(v)

                for v in item.values()

            ).strip()

            if value:

                result.append(value)

        else:

            value = str(item).strip()

            if value:

                result.append(value)

    return result


def parse_response(
    response: str
) -> dict:
    """
    Parse Mistral response.
    """

    if not response:

        return {

            "summary": "",

            "keywords": [],

            "entities": [],

            "sentiment": "Neutral",

            "topics": [],

            "recommendations": []

        }

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

            return {

                "summary": str(

                    data.get(

                        "summary",

                        ""

                    )

                ),

                "keywords": normalize_list(

                    data.get(

                        "keywords",

                        []

                    )

                ),

                "entities": normalize_list(

                    data.get(

                        "entities",

                        []

                    )

                ),

                "sentiment": str(

                    data.get(

                        "sentiment",

                        "Neutral"

                    )

                ),

                "topics": normalize_list(

                    data.get(

                        "topics",

                        []

                    )

                ),

                "recommendations": normalize_list(

                    data.get(

                        "recommendations",

                        []

                    )

                )

            }

        except Exception:

            pass

    # --------------------------------------------------
    # Fallback
    # --------------------------------------------------

    return {

        "summary": response,

        "keywords": [],

        "entities": [],

        "sentiment": "Neutral",

        "topics": [],

        "recommendations": []

    }