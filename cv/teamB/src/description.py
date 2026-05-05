import base64
import httpx
import asyncio

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:latest"

async def call_ollama(payload):
    for i in range(3):
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                res = await client.post(OLLAMA_URL, json=payload)
                return res
        except Exception as e:
            print(f"Retry {i+1}:", e)
            await asyncio.sleep(1)
    return None

async def describe_image_bytes(contents: bytes):
    try:
        image_b64 = base64.b64encode(contents).decode()

        payload = {
            "model": MODEL,
            "prompt": "Describe this image in one simple sentence.",
            "images": [image_b64],
            "stream": False
        }

        res = await call_ollama(payload)

        if res is None:
            return "Model not responding"

        print("DESC RAW:", res.text)

        data = res.json()
        desc = data.get("response", "").strip()

        return desc if desc else "No description"

    except Exception as e:
        print("DESC ERROR:", e)
        return "Description failed"