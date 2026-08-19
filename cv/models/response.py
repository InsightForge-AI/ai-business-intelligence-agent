"""
==========================================================
CV Response Model
==========================================================

Standard response model for Computer Vision analysis.
"""

from typing import Dict
from typing import List

from pydantic import BaseModel


class CVResponse(BaseModel):
    """
    Computer Vision response.
    """

    module: str

    success: bool

    document_type: str

    extracted_text: str

    fields: Dict

    tables: List

    charts: List

    confidence: float

    message: str