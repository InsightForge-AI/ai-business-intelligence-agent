from fastapi import FastAPI, UploadFile, File, HTTPException
from integration.main import process_image
import shutil
from pathlib import Path
import uuid

app = FastAPI(title="CV Pipeline API")

# upload folder
UPLOAD_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # ✅ validation
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")

        if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            raise HTTPException(status_code=400, detail="Only image files allowed")

        # ✅ unique filename (IMPORTANT)
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_name

        # ✅ save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ close file
        file.file.close()

        # ✅ run pipeline
        result = process_image(file_path)

        # 🔥 cleanup temp file
        try:
            file_path.unlink()
        except:
            pass

        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))