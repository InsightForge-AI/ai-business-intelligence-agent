import base64
import httpx
import asyncio

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:latest"

async def call_ollama(payload):
    for i in range(3):  # 🔁 retry 3 times
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                res = await client.post(OLLAMA_URL, json=payload)
                return res
        except Exception as e:
            print(f"Retry {i+1}:", e)
            await asyncio.sleep(1)
    return None

async def analyze_image_bytes(contents: bytes):
    try:
        image_b64 = base64.b64encode(contents).decode()

        payload = {
            "model": MODEL,
            "prompt": "List 3-5 objects in this image as simple words separated by commas.",
            "images": [image_b64],
            "stream": False
        }

        res = await call_ollama(payload)

        if res is None:
            return ["model not responding"]

        print("LABEL RAW:", res.text)

        data = res.json()
        raw = data.get("response", "").lower().strip()

        if not raw:
            return ["no objects"]

        raw = raw.replace("\n", " ").replace(".", "")

        labels = raw.split(",") if "," in raw else raw.split()

        return [x.strip() for x in labels if len(x.strip()) > 2]

    except Exception as e:
        print("LABEL ERROR:", e)
        return ["labeling failed"]