import requests
from config import RAG_API_URL, REQUEST_TIMEOUT

def run_rag(query):
    response = requests.post(
        RAG_API_URL,
        json={"query" : query},
        timeout=REQUEST_TIMEOUT
    )

    return response.json()