import sys
from pathlib import Path

# 🔥 Fix import path (VERY IMPORTANT)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ⬇️ Imports
from fastapi import FastAPI, UploadFile, File
from src.image_analysis import analyze_image

app = FastAPI()


# 🚀 CV API
@app.post("/cv/analyze")
async def cv_analyze(file: UploadFile = File(None)):
    return await analyze_image(file)