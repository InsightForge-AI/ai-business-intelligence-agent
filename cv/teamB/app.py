from fastapi import FastAPI, UploadFile, File
from integration.main import process_image
import shutil
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 TEMP FIX (disable heavy parts)
        result = {
            "image": file.filename,
            "objects": ["fish", "bee"],
            "extracted_text": ["sample text"],
            "description": "Sample caption"
        }

        return result

    except Exception as e:
        return {"error": str(e)}