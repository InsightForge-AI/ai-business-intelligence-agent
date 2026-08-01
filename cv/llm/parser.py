"""
==========================================================
Llama Response Parser
==========================================================

Responsibilities
----------------
• Parse Llama response
• Extract valid JSON
• Return fallback response
"""

import json
import re


def parse_response(
    response: str
) -> dict:
    """
    Parse Llama response.

    Parameters
    ----------
    response : str

    Returns
    -------
    dict
    """

    if not response:

        return {

            "document_type": "Unknown",

            "extracted_text": "",

            "fields": {},

            "key_values": {},

            "tables": [],

            "charts": [],

            "confidence": 0.0

        }

    # -----------------------------------------------------
    # Remove Markdown
    # -----------------------------------------------------

    response = re.sub(

        r"```json|```",

        "",

        response

    ).strip()

    # -----------------------------------------------------
    # Extract JSON Object
    # -----------------------------------------------------

    match = re.search(

        r"\{.*\}",

        response,

        re.DOTALL

    )

    if not match:

        return {

            "document_type": "Unknown",

            "extracted_text": "",

            "fields": {},

            "key_values": {},

            "tables": [],

            "charts": [],

            "confidence": 0.0

        }

    # -----------------------------------------------------
    # Parse JSON
    # -----------------------------------------------------

    try:

        data = json.loads(

            match.group()

        )

        return {

            "document_type": data.get(

                "document_type",

                "Unknown"

            ),

            "extracted_text": data.get(

                "extracted_text",

                ""

            ),

            "fields": data.get(

                "fields",

                {}

            ),

            "key_values": data.get(

                "key_values",

                {}

            ),

            "tables": data.get(

                "tables",

                []

            ),

            "charts": data.get(

                "charts",

                []

            ),

            "confidence": float(

                data.get(

                    "confidence",

                    0.0

                )

            )

        }

    except Exception:

        return {

            "document_type": "Unknown",

            "extracted_text": "",

            "fields": {},

            "key_values": {},

            "tables": [],

            "charts": [],

            "confidence": 0.0

        }