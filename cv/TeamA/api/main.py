from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
import cv2
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "data", "uploads")
TEAM_A_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(os.path.join(TEAM_A_DIR))
# ✅ Import your existing modules (TeamA)
from src.preprocessing import preprocess_image
from src.objectdetection import detect_objects
from src.imageclassification import classify_image
app = FastAPI()
os.makedirs(UPLOAD_DIR, exist_ok=True)
def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Invalid image"}
    processed = preprocess_image(image_path)
    processed = (processed * 255).astype("uint8")
    processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    detected = detect_objects(image_path)
    classified = classify_image(image_path)
    return {
        "message": "Processing Done",
        "details": "Preprocessing + Detection + Classification completed"
    }


# ===== API ROUTE =====
@app.post("/process/")
async def process(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_image(file_path)

    return JSONResponse(content=result)


# ===== SIMPLE UI =====
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h2>TeamA CV Pipeline</h2>
            <form action="/process/" method="post" enctype="multipart/form-data">
                <input type="file" name="file"/>
                <input type="submit"/>
            </form>
        </body>
    </html>
    """