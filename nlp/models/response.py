"""
==========================================================
NLP Response Model
==========================================================

Standard NLP response.
"""

from typing import List

from pydantic import BaseModel


class NLPResponse(BaseModel):

    module: str

    success: bool

    summary: str

    keywords: List[str]

    entities: List[str]

    sentiment: str

    topics: List[str]

    recommendations: List[str]

    message: str