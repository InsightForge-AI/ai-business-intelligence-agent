from fastapi import FastAPI
from src.search import search

app = FastAPI()

@app.post("/rag/query")
def rag(data: dict):
    return {"context": search(data["query"])}