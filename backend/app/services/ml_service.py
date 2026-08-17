import requests
from config import ML_API_URL, REQUEST_TIMEOUT

def run_ml(query):
    response = requests.post(
        ML_API_URL,
        json={"data" : query},
        timeout=REQUEST_TIMEOUT
    )

    return response.json()