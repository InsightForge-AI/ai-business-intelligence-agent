import sys
from pathlib import Path

# 🔥 FIX PATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, UploadFile, File
from src.image_analysis import analyze_image
import shutil

app = FastAPI()

UPLOAD_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return analyze_image(file_path)
from fastapi import FastAPI, UploadFile, File
from src.image_analysis import analyze_image

app = FastAPI()

@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    return analyze_image(file)
