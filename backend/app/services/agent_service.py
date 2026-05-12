import requests
from config import AGENT_API_URL


def run_agent(query):

    try:

        response = requests.post(
            AGENT_API_URL,
            json={"query": query},
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        return ["nlp"]