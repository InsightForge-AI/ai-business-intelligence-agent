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
    results = search(request.query, model, collection)

    return {
        "query": request.query,
        "answers": results
    }