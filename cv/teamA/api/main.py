from fastapi import FastAPI, UploadFile, File
import os
import shutil

from cv.teamA.src.vision import VisionAnalyzer

app = FastAPI()

vision = VisionAnalyzer()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Sprint-4 AI System Running 🚀"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # ✅ Correct call
        result = vision.analyze(file_path)

        return result

    except Exception as e:
        return {"error": str(e)}