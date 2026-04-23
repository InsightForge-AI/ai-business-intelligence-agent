import requests
from config import AGENT_API_URL

def run_agent(query):
    response = requests.post(
        AGENT_API_URL,
        json={"query" : query}
    )

    return response.json()