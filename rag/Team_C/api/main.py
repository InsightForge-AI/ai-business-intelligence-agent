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

    results = simple_search(request.query)

    return {
        "query": request.query,
        "total_results": len(results),
        "results": results
    }