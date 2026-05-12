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

            print(f"Retry {i+1}:", e)

            await asyncio.sleep(2)

    return None


# ✅ Main labeling function
async def analyze_image_bytes(contents: bytes):

    try:
        # ✅ Convert image to base64
        image_b64 = base64.b64encode(contents).decode("utf-8")

        payload = {
            "model": MODEL,
            "prompt": (
                "Look at this image and return only 3 to 5 object names "
                "separated by commas."
            ),
            "images": [image_b64],
            "stream": False
        }

        # ✅ Call Ollama
        response = await call_ollama(payload)

        if response is None:
            return ["model not responding"]

        print("LABEL RESPONSE:", response.text)

        # ✅ Parse response
        data = response.json()

        raw = data.get("response", "").strip().lower()

        if not raw:
            return ["no objects detected"]

        # ✅ Clean response
        raw = (
            raw.replace("\n", " ")
               .replace(".", "")
               .replace("objects:", "")
               .replace("labels:", "")
        )

        # ✅ Split labels
        if "," in raw:
            labels = raw.split(",")
        else:
            labels = raw.split()

        # ✅ Final clean labels
        final_labels = []

        for label in labels:

            label = label.strip()

            if len(label) > 1:
                final_labels.append(label)

        # ✅ Remove duplicates
        final_labels = list(dict.fromkeys(final_labels))

        return final_labels[:5]

    except Exception as e:

        print("LABELING ERROR:", e)

        return ["labeling failed"]