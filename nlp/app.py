from fastapi import FastAPI, UploadFile, File
import os
import uuid

from processor import process_file

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "tests")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/nlp/analyze")
async def analyze_file(file: UploadFile = File(...)):

    try:

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        temp_path = os.path.join(
            UPLOAD_DIR,
            unique_name
        )

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        result = process_file(temp_path)

        return result

    except Exception:

        return {
            "sentiment": "neutral",
            "summary": "processing error",
            "keywords": []
        }