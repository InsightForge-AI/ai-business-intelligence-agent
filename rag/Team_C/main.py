from fastapi import FastAPI

from rag.Team_C.preprocessing.clean_query import clean_query
from rag.Team_C.retrieval.retriever import retrieve_documents
from rag.Team_C.ranking.ranker import rank_results
from rag.Team_C.response_builder.builder import build_response

app = FastAPI()

@app.post("/rag/query")
def rag_query(data: dict):

    query = data.get("query")
    top_k = data.get("top_k", 3)

    tokens = clean_query(query)

    retrieved_docs = retrieve_documents(tokens)

    ranked_docs = rank_results(retrieved_docs)

    response = build_response(query, ranked_docs, top_k)

    return response