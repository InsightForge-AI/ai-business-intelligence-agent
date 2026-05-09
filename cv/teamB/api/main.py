from fastapi import FastAPI, UploadFile, File
from cv.teamB.src.integration import process_image

app = FastAPI()

@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # ✅ Direct processing
        result = await process_image(file)

        # ✅ Return exact API contract
        return result

    except Exception as e:
        return {
            "text": "",
            "labels": [],
            "description": "",
            "error": str(e)
        }