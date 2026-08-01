"""
==========================================================
RAG Request Model
==========================================================

Request model for RAG analysis.
"""

from typing import Dict

from pydantic import BaseModel


class RAGRequest(BaseModel):
    """
    RAG request.
    """

    query: str

    content: str

    metadata: Dict = {}