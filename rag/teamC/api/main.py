from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# allow imports from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.search import simple_search

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "AI_Business_Intelligent_Agent Simple RAG API is running!"}


@app.post("/rag/query")
def rag_query(request: QueryRequest):

    query = request.query

    # Case 1 — empty query
    if not query or not query.strip():
        return {
            "query": request.query,
            "total_results": 0,
            "message": "empty query",
            "results": []
        }

    results = simple_search(query)

    # Case 2 — no match
    if len(results) == 0:
        return {
            "query": request.query,
            "total_results": 0,
            "message": "not found",
            "results": []
        }

    return {
        "query": request.query,
        "total_results": len(results),
        "results": results
    }