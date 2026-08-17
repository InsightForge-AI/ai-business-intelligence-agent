import base64
import binascii

import requests
from config import CV_API_URL, REQUEST_TIMEOUT


def run_cv(file_name, file_data_b64):
    """Forward an uploaded image (as base64) to the CV service.

    `file_name`/`file_data_b64` come from the actual uploaded file's bytes
    (see AnalyzeRequest.file_data in backend/app/api/analyze.py) -- this no
    longer accepts a free-text query as a filesystem path.
    """

    if not file_data_b64:
        return {"error": "No image file was uploaded"}

    try:
        file_bytes = base64.b64decode(file_data_b64, validate=True)
    except (binascii.Error, ValueError):
        return {"error": "Uploaded file data is not valid base64"}

    files = {
        "file": (file_name or "upload.png", file_bytes, "application/octet-stream")
    }

    response = requests.post(
        CV_API_URL,
        files=files,
        timeout=REQUEST_TIMEOUT
    )

    return response.json()
