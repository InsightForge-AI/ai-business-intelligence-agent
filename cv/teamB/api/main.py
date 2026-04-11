from fastapi import FastAPI, UploadFile, File
from src.image_analysis import analyze_image

app = FastAPI()

@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    return analyze_image(file)