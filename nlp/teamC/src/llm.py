import requests
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

MODEL_NAME = "mistral"

URL = "http://localhost:11434/api/generate"


def ask_llm(prompt):

    try:

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        logger.info("Sending request to local LLM")

        response = requests.post(
            URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        logger.info("LLM response received")

        return result.get("response", "").strip()

    except Exception as e:

        logger.error(f"LLM Error: {e}")

        return None