import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(model: str, prompt: str):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "No response from model"
        )

    except requests.exceptions.ConnectionError:

        return "LLM Error: Ollama server not running"

    except requests.exceptions.Timeout:

        return "LLM Error: Request timeout"

    except requests.exceptions.HTTPError as e:

        return f"LLM HTTP Error: {str(e)}"

    except Exception as e:

        return f"LLM Error: {str(e)}"