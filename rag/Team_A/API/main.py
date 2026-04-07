from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pipeline.rag_pipeline import search_pipeline
from search_logic.search import search

app = FastAPI()

# Load cleaned data
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "document_cleaned.json")
with open(file_path, "r", encoding="utf-8") as f:
    documents = json.load(f)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "AI Business Intelligence Agent API is running!"}

@app.post("/search/keyword")
def keyword_search(request: QueryRequest):
    results = search(request.query, documents)
    return {"query": request.query, "results": results}

@app.post("/search/semantic")
def semantic_search(request: QueryRequest):
    results = search_pipeline(request.query)
    return {"query": request.query, "results": results}