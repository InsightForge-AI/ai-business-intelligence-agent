from fastapi.responses import JSONResponse
from PIL import Image
import io

SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


async def analyze_image(file):

    if file is None:
        return {
            "objects": [],
            "extracted_text": "No file provided",
            "description": "No image input"
        }

    if file.content_type not in SUPPORTED_TYPES:
        return {
            "objects": [],
            "extracted_text": "Invalid format",
            "description": "Unsupported file type"
        }

    try:
        contents = await file.read()

        if len(contents) == 0:
            return {
                "objects": [],
                "extracted_text": "Empty file",
                "description": "Uploaded file is empty"
            }

        Image.open(io.BytesIO(contents)).verify()

        # success output
        return {
            "objects": ["box"],
            "extracted_text": "sample text",
            "description": "basic image"
        }

    except Exception:
        return {
            "objects": [],
            "extracted_text": "Invalid image",
            "description": "Corrupt or unreadable image"
        }
        }
def analyze_image(image_path):
    return {
        "objects": detect_objects(image_path),
        "extracted_text": extract_text(image_path),
        "description": describe_image(image_path)
    }
def analyze_image(image):
    return {
        "objects": ["box"],
        "extracted_text": "sample",
        "description": "basic image"
    }
