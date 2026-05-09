import requests
from config import ML_API_URL


def run_ml(query):

    try:

        response = requests.post(
            ML_API_URL,
            json={"query": query},
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }