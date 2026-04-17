import sys
from pathlib import Path

# 🔥 FIX PATH (IMPORTANT)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ⬇️ Imports
from fastapi import FastAPI, UploadFile, File
from src.image_analysis import analyze_image
import shutil
from PIL import Image

app = FastAPI()

# 📁 Temp folder for uploads
UPLOAD_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)


# ✅ Validation Function
def check_image(file: UploadFile):
    
    if file is None:
        return "No image provided"
    
    if file.filename == "":
        return "Empty file"
    
    if not file.filename.lower().endswith(("jpg", "jpeg", "png")):
        return "Invalid format"
    
    return "valid"


# 🚀 API Endpoint
@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    
    # ✅ Step 1: Validation
    valid = check_image(file)
    if valid != "valid":
        return {
            "status": "error",
            "message": valid
        }

    file_path = UPLOAD_DIR / file.filename

    try:
        # ✅ Step 2: Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Step 3: Corrupt image check
        try:
            img = Image.open(file_path)
            img.verify()
        except:
            return {
                "status": "error",
                "message": "Corrupt image"
            }

        # ✅ Step 4: Call existing logic
        result = analyze_image(file_path)

        # ✅ Step 5: Success response
        return {
            "status": "success",
            "result": result
        }

    except Exception:
        return {
            "status": "error",
            "message": "Processing failed"
        }