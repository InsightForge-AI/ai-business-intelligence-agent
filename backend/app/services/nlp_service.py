import requests
from config import NLP_API_URL


def run_nlp(query):

    try:

        response = requests.post(
            NLP_API_URL,
            json={"text": query},
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }