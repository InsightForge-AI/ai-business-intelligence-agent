import requests

def call_llm(prompt: str) -> str:
    # 90-second timeout to allow i7 to process full R1 reasoning
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1", 
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,  # Lower temperature for realistic consistency
                    "num_predict": 512    # Prevents excessively long thinking
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"DEBUG: LLM Connection issue: {e}")
        return None