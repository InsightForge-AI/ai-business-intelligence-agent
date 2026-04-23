import requests
from config import RAG_API_URL

def run_rag(query):
    response = requests.post(
        RAG_API_URL,
        json={"query" : query}
    )

    return response.json()