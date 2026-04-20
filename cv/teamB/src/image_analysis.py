from fastapi.responses import JSONResponse
from PIL import Image
import io

SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


async def analyze_image(file):

    # edge case: no file
    if file is None:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "No image provided",
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )

    # edge case: unsupported format
    if file.content_type not in SUPPORTED_TYPES:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Unsupported file format",
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )

    try:
        contents = await file.read()

        # empty file check
        if len(contents) == 0:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Empty file",
                    "objects": [],
                    "extracted_text": "",
                    "description": ""
                }
            )

        # corrupt image check
        Image.open(io.BytesIO(contents)).verify()

        # 👉 Yaha actual logic hona chahiye (future)
        return {
            "status": "success",
            "objects": ["box"],  # temporary
            "extracted_text": "sample",
            "description": "basic image"
        }

    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Invalid or corrupt image",
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )