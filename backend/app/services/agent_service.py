import requests
from config import AGENT_API_URL, REQUEST_TIMEOUT

def run_agent(query):
    response = requests.post(
        AGENT_API_URL,
        json={"query" : query},
        timeout=REQUEST_TIMEOUT
    )

    return response.json()