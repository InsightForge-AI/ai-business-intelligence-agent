from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# allow imports from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.search import simple_search,generate_llm_answer

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "AI_Business_Intelligent_Agent Simple RAG API is running!"}


@app.post("/rag/query")
def rag_query(request: QueryRequest):

    query = request.query

    query = request.query

    # ------------------------
    # EDGE CASE: EMPTY
    # ------------------------
    if not query or not query.strip():
        return {
            "query": query,
            "answer": "",
            "content": [],
            "total_results": 0,
            "message": "empty query"
        }

    results = simple_search(query)

    # ------------------------
    # EDGE CASE: NO MATCH
    # ------------------------
    if len(results) == 0:
        return {
            "query": query,
            "answer": "",
            "content": [],
            "total_results": 0,
            "message": "not found"
        }

    # ------------------------
    # LLM ANSWER
    # ------------------------
    answer = generate_llm_answer(query, results)

    return {
        "query": query,
        "answer": answer,
        "content": [r["text"] for r in results],
        "total_results": len(results)
    }