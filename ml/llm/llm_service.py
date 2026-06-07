import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def call_llm(model: str, prompt: str):
    """Send prompt to Ollama model."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 1000
                }
            },
            timeout=600
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")

    except requests.exceptions.RequestException as e:
        print("LLM Request Error:", e)
        return None

    except (ValueError, KeyError) as e:
        print("Invalid Response:", e)
        return None