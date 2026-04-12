from detect import detect_objects
from ocr import extract_text
from describe import describe_image
from fastapi import FastAPI, UploadFile, File
import shutil
app = FastAPI()
import os

def analyze_image(image_path):
    description = describe_image(image_path)
    objects = detect_objects(image_path)
    text = extract_text(image_path)
    return {
        "objects": objects,
        "text": text,
        "description": description
    }
    
@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/analyze")
async def analyze(file: UploadFile=File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = analyze_image(file_path)
    os.remove(file_path)
    return result    
