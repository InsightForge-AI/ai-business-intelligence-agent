"""
==========================================================
CV Formatter
==========================================================

Responsibilities
----------------
• Format CV analysis
• Standardize output
"""

from typing import Dict
from typing import List


def format_analysis(
    document_type: str,
    extracted_text: str,
    fields: Dict,
    key_values: Dict,
    tables: List,
    charts: List,
    confidence: float
) -> dict:
    """
    Format Computer Vision analysis.

    Parameters
    ----------
    document_type : str

    extracted_text : str

    fields : dict

    key_values : dict

    tables : list

    charts : list

    confidence : float

    Returns
    -------
    dict
    """

    return {

        "document_type": document_type,

        "extracted_text": extracted_text,

        "fields": fields,

        "key_values": key_values,

        "tables": tables,

        "charts": charts,

        "confidence": confidence

    }