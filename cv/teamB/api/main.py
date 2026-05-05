<<<<<<< HEAD
import sys
from pathlib import Path

# 🔥 FIX PATH (IMPORTANT)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ⬇️ Imports
=======
>>>>>>> f841ba2 (Removed image_analysis module)
from fastapi import FastAPI, UploadFile, File
from src.integration import process_image

app = FastAPI()

<<<<<<< HEAD
@app.post("/cv/analyze")
async def cv_analyze(file: UploadFile = File(None)):
    return await analyze_image(file)

app = FastAPI()   # ✅ IMPORTANT

@app.post("/cv/analyze")
async def cv_analyze(file: UploadFile = File(None)):
    return await analyze_image(file)
import shutil
from PIL import Image

app = FastAPI()

# 📁 Temp folder for uploads
UPLOAD_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)


# ✅ Validation Function
def check_image(file: UploadFile):
    
    if file is None:
        return "not found"
    
    if file.filename == "" or file.filename is None:
        return "not found"
    
    if not file.filename.lower().endswith(("jpg", "jpeg", "png")):
        return "Invalid format"
    
    return "valid"


# 🚀 API Endpoint
@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(None)):
    
    # ✅ Step 1: Validation
    valid = check_image(file)
    if valid != "valid":
        return {
            "status": "error",
            "message": valid,
            "file_name": file.filename if file else None
        }

    file_path = UPLOAD_DIR / file.filename

    try:
        # ✅ Step 2: Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ NEW: Empty file check 🔥
        if file_path.stat().st_size == 0:
            return {
                "status": "error",
                "message": "Empty file",
                "file_name": file.filename
            }

        # ✅ Step 3: Corrupt image check
        try:
            img = Image.open(file_path)
            img.verify()
        except:
            return {
                "status": "error",
                "message": "Corrupt image",
                "file_name": file.filename
            }

        # ✅ Step 4: Call existing logic
        result = analyze_image(file_path)

        # ✅ Step 5: Handle empty result
        if not result:
            return {
                "status": "error",
                "message": "not found",
                "file_name": file.filename
            }

        # ✅ Step 6: Success response
        return {
            "status": "success",
            "file_name": file.filename,
            "result": result
        }

    except Exception:
        return {
            "status": "error",
            "message": "Processing failed",
            "file_name": file.filename if file else None
        }
=======
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # Direct file pass karo (no manual save needed)
        result = await process_image(file)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
>>>>>>> f841ba2 (Removed image_analysis module)
