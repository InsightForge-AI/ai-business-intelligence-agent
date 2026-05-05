from fastapi import FastAPI, UploadFile, File
from src.integration import process_image

app = FastAPI()

@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # ✅ Direct processing
        result = await process_image(file)

        # ✅ Return EXACT API contract (no extra fields)
        return result

    except Exception as e:
        return {
            "text": "",
            "labels": [],
            "description": "",
            "error": str(e)
        }