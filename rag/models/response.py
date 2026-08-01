"""
==========================================================
RAG Response Model
==========================================================

Standard response model.
"""

from typing import List

from pydantic import BaseModel


class Source(BaseModel):
    """
    Source information.
    """

    chunk: int

    page: int


class RAGResponse(BaseModel):
    """
    Standard RAG response.
    """

    module: str

    success: bool

    answer: str

    sources: List[Source]

    confidence: float

    message: str