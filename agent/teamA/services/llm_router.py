import ast
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

VALID_MODULES = {"nlp", "ml", "cv", "rag"}


def refine_module_decision(
    query: str,
    detected_modules: list[str]
) -> list[str]:
    """
    Uses LLaMA3 via Ollama to validate/refine module routing.
    Falls back safely to rule-based routing.
    """

    prompt = f"""
You are an intelligent routing assistant.

User Query:
{query}

Rule-Based Detected Modules:
{detected_modules}

Available Modules:
- nlp
- ml
- cv
- rag

Task:
- Validate or refine routing
- Return ONLY a Python list
- Example:
["nlp","ml"]

Rules:
- No explanation
- No markdown
- No extra text
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )

        data = response.json()

        output = data.get("response", "").strip()

        parsed = ast.literal_eval(output)

        if isinstance(parsed, list):

            cleaned = [
                module
                for module in parsed
                if module in VALID_MODULES
            ]

            if cleaned:
                return cleaned

    except Exception:
        pass

    # Safe fallback
    return detected_modules