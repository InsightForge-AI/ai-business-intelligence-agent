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
                "error": "No image provided",
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
                "error": "Unsupported file format",
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )

    try:
        contents = await file.read()

        # check corrupt image
        Image.open(io.BytesIO(contents)).verify()

        # dummy output
        return {
            "objects": ["box"],
            "extracted_text": "sample",
            "description": "basic image"
        }

    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid or corrupt image",
                "objects": [],
                "extracted_text": "",
                "description": ""
            }
        )