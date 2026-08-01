"""
==========================================================
CV Validator
==========================================================

Responsibilities
----------------
• Validate formatted CV analysis
• Ensure required fields exist
• Apply default values
"""

from utils.constants import DOCUMENT_TYPES


def validate_analysis(
    analysis: dict
) -> dict:
    """
    Validate Computer Vision analysis.

    Parameters
    ----------
    analysis : dict

    Returns
    -------
    dict
    """

    if analysis is None:

        analysis = {}

    # -----------------------------------------------------
    # Document Type
    # -----------------------------------------------------

    document_type = analysis.get(

        "document_type",

        "Unknown"

    )

    if document_type not in DOCUMENT_TYPES:

        document_type = "Unknown"

    # -----------------------------------------------------
    # Extracted Text
    # -----------------------------------------------------

    extracted_text = analysis.get(

        "extracted_text",

        ""

    )

    # -----------------------------------------------------
    # Fields
    # -----------------------------------------------------

    fields = analysis.get(

        "fields",

        {}

    )

    if not isinstance(

        fields,

        dict

    ):

        fields = {}

    # -----------------------------------------------------
    # Key Values
    # -----------------------------------------------------

    key_values = analysis.get(

        "key_values",

        {}

    )

    if not isinstance(

        key_values,

        dict

    ):

        key_values = {}

    # -----------------------------------------------------
    # Tables
    # -----------------------------------------------------

    tables = analysis.get(

        "tables",

        []

    )

    if not isinstance(

        tables,

        list

    ):

        tables = []

    # -----------------------------------------------------
    # Charts
    # -----------------------------------------------------

    charts = analysis.get(

        "charts",

        []

    )

    if not isinstance(

        charts,

        list

    ):

        charts = []

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    confidence = analysis.get(

        "confidence",

        0.0

    )

    try:

        confidence = float(

            confidence

        )

    except Exception:

        confidence = 0.0

    confidence = max(

        0.0,

        min(

            confidence,

            1.0

        )

    )

    # -----------------------------------------------------
    # Final Output
    # -----------------------------------------------------

    return {

        "document_type": document_type,

        "extracted_text": extracted_text,

        "fields": fields,

        "key_values": key_values,

        "tables": tables,

        "charts": charts,

        "confidence": confidence

    }