import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def call_llm(model, prompt):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")

    except Exception as e:

        print("LLM ERROR:", e)

        return None