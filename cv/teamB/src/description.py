import base64
import httpx
import asyncio

# ✅ Ollama Config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:latest"


# ✅ Retry helper
async def call_ollama(payload):
    for i in range(3):
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(
                    OLLAMA_URL,
                    json=payload
                )

                response.raise_for_status()

                return response

        except Exception as e:
            print(f"[Retry {i+1}] Description Error:", e)
            await asyncio.sleep(2)

    return None


# ✅ Main function used in integration
async def run_description(file):

    try:
        # ✅ Read image
        contents = await file.read()

        # ✅ Reset pointer
        await file.seek(0)

        # ✅ Convert to base64
        image_b64 = base64.b64encode(contents).decode("utf-8")

        payload = {
            "model": MODEL,
            "prompt": (
                "Describe this image in one clear simple sentence."
            ),
            "images": [image_b64],
            "stream": False
        }

        # ✅ Call Ollama
        response = await call_ollama(payload)

        if response is None:
            return "Model not responding"

        print("DESCRIPTION RESPONSE:", response.text)

        # ✅ Parse JSON
        data = response.json()

        desc = data.get("response", "").strip()

        if not desc:
            return "No description"

        # ✅ Clean response
        desc = (
            desc.replace("\n", " ")
                .replace("Description:", "")
                .strip()
        )

        return desc

    except Exception as e:
        print("DESCRIPTION ERROR:", e)

        return "Description failed"