"""
==========================================================
CV Request Model
==========================================================

Request model for Computer Vision analysis.
"""

from typing import Dict
from pydantic import BaseModel


class CVRequest(BaseModel):
    """
    Computer Vision request.
    """

    query: str

    content: str

    metadata: Dict = {}