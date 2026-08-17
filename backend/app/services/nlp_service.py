import requests
from config import NLP_API_URL, REQUEST_TIMEOUT

def run_nlp(query):
    response = requests.post(
        NLP_API_URL,
        json={"text" : query},
        timeout=REQUEST_TIMEOUT
    )

    return response.json()