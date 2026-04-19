# This module is done by Vaishnavi

from fastapi import APIRouter
from pydantic import BaseModel

from rag.Team_D.app.services.retrieval import search
from rag.Team_D.app.services.embedding import model

router = APIRouter()

collection = None  # will be initialized at startup


class QueryRequest(BaseModel):
    query: str


@router.post("/rag/query")
def ask_question(request: QueryRequest):
    """
    Query the RAG system with proper edge case handling for:
    - Normal queries
    - Empty queries
    - Case sensitivity
    - Extra spaces
    - Duplicate words
    - Partial matches
    - Long queries
    - No matches
    """
    results = search(request.query, model, collection)
    return results