import requests
from config import RAG_API_URL


def run_rag(query):

    try:

        response = requests.post(
            RAG_API_URL,
            json={"query": query},
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }