# FastAPI entrypoint placeholder

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from rag.Team_D.load_data.load_data import load_faq_data
from rag.Team_D.embedding.embedding import get_embeddings, model
from rag.Team_D.retrieval.retrievl import create_collection, search

app = FastAPI()


docs = load_faq_data(r"rag\Team_D\data\faq.txt")
embeddings = get_embeddings(docs)
collection = create_collection(docs, embeddings)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "RAG API running"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    results = search(request.query, model, collection)

    return {
        "query": request.query,
        "answers": results
    }