import requests
from config import ML_API_URL

def run_ml(query):
    response = requests.post(
        ML_API_URL,
        json={"data" : query}
    )

    return response.json()