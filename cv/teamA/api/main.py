from fastapi import FastAPI, UploadFile, File
from teamA.src.image_analysis import analyze_image

app = FastAPI()

@app.post("/cv/analyze")
async def cv_analyze(file: UploadFile = File(None)):
    return await analyze_image(file)
