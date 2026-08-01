"""
==========================================================
NLP Request Model
==========================================================

Request model for NLP analysis.
"""

from typing import Dict

from pydantic import BaseModel


class NLPRequest(BaseModel):
    """
    NLP request.
    """

    query: str

    content: str

    metadata: Dict = {}