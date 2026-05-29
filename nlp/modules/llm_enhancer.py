import requests

MODEL_NAME = "mistral"

URL = "http://localhost:11434/api/generate"

def ask_llm(prompt):

    try:

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            URL,
            json=payload,
            timeout=60
        )

        result = response.json()

        return result.get("response", "").strip()

    except Exception as e:

        print("LLM Error:", e)

        return None
