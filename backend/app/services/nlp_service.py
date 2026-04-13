import requests
from config import NLP_API_URL

def run_nlp(query):
    response = requests.post(
        NLP_API_URL,
        json={"text" : query}
    )

    return response.json()