import base64
import httpx
import asyncio

# ✅ Ollama Config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:latest"


# ✅ Retry function
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
            print(f"[Retry {i+1}] Ollama Error:", e)
            await asyncio.sleep(2)

    return None


# ✅ Main labeling function
async def analyze_image(file):
    """
    Takes FastAPI UploadFile
    Returns list of labels
    """

    try:
        # ✅ Read image
        contents = await file.read()

        # ✅ Reset pointer for reuse
        await file.seek(0)

        # ✅ Convert image to base64
        image_b64 = base64.b64encode(contents).decode("utf-8")

        # ✅ Prompt
        payload = {
            "model": MODEL,
            "prompt": (
                "Look at this image carefully and identify only the main objects. "
                "Return ONLY 3 to 5 object names separated by commas. "
                "Example: person, car, dog"
            ),
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

        # ✅ Call Ollama
        response = await call_ollama(payload)

        if response is None:
            return ["model not responding"]

        # ✅ Debug response
        print("LABEL RESPONSE:", response.text)

        # ✅ Parse response
        data = response.json()

        raw = data.get("response", "").strip().lower()

        if not raw:
            return ["no objects detected"]

        # ✅ Clean output
        raw = (
            raw.replace("\n", " ")
               .replace(".", "")
               .replace("objects:", "")
               .replace("labels:", "")
        )

        # ✅ Split labels
        labels = []

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

        # ✅ Limit output
        return final_labels[:5] if final_labels else ["no objects detected"]

    except Exception as e:
        print("LABELING ERROR:", e)

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