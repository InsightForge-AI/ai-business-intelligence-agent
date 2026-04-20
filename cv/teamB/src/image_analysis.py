from fastapi.responses import JSONResponse
from PIL import Image
import io

SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


async def analyze_image(file):

    if file is None:
        return JSONResponse(
            status_code=400,
            content={
                
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )

    if file.content_type not in SUPPORTED_TYPES:
        return JSONResponse(
            status_code=400,
            content={
                
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )

    try:
        contents = await file.read()

        if len(contents) == 0:
            return JSONResponse(
                status_code=400,
                content={
                    
                    "objects": [],
                    "extracted_text": "",
                    "description": ""
                }
            )

        Image.open(io.BytesIO(contents)).verify()

        return {
            
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