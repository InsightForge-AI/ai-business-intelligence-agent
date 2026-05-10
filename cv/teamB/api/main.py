from fastapi import FastAPI, UploadFile, File
<<<<<<< HEAD
from cv.teamB.src.integration import process_image
from src.integration import process_image
=======
from teamB.src.integration import process_image
>>>>>>> 9e002aa (Updated import paths for backend integration)

app = FastAPI()

@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # ✅ Direct processing
        result = await process_image(file)

        # ✅ Return exact API contract
        # ✅ Return EXACT API contract (no extra fields)
        return result

    except Exception as e:
        return {
            "text": "",
            "labels": [],
            "description": "",
            "error": str(e)
        }