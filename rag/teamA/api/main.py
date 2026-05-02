from fastapi import FastAPI
from src.search import search

app = FastAPI(title="RAG API", version="1.0")

@app.post("/rag/query")
def rag(data: dict):
    try:
        query = data.get("query", "")
        return search(query)
    except Exception as e:
        return {
            "content": [],
            "total_results": 0,
            "message": f"error: {str(e)}"
        }