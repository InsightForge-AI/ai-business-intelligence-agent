import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from PIL import Image
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..src.image_analysis import analyze_image

app = FastAPI()


class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    """Rejects uploads whose declared Content-Length exceeds a cap.

    Nothing enforced a size limit before -- any upload size was accepted
    and fully buffered to disk before validation. Content-Length check
    only (not streaming enforcement), same tradeoff as backend/main.py.
    """

    def __init__(self, app, max_bytes):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request, call_next):
        content_length = request.headers.get("content-length")
        if content_length is not None and int(content_length) > self.max_bytes:
            return JSONResponse(
                {"error": "Request body too large"}, status_code=413
            )
        return await call_next(request)


app.add_middleware(MaxBodySizeMiddleware, max_bytes=10 * 1024 * 1024)

# Upload folder anchored to this module's own location, not the process's
# current working directory (which varies depending on how the service is
# launched -- run.py, a direct uvicorn invocation, or a test runner).
UPLOAD_DIR = Path(__file__).resolve().parent / "temp"
UPLOAD_DIR.mkdir(exist_ok=True)


def check_image(file: UploadFile):

    if file is None:
        return "not found"

    if file.filename == "" or file.filename is None:
        return "not found"

    if not file.filename.lower().endswith(("jpg", "jpeg", "png")):
        return "Invalid format"

    return "valid"


@app.post("/cv/analyze")
async def analyze(file: UploadFile = File(None)):

    # Step 1: Validation
    valid = check_image(file)
    if valid != "valid":
        return {
            "status": "error",
            "message": valid,
            "file_name": file.filename if file else None
        }

    # Strip any directory components from the untrusted filename so it can
    # never escape UPLOAD_DIR (e.g. "../../evil.png" -> "evil.png").
    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name

    try:
        # Step 2: Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 3: Empty file check
        if file_path.stat().st_size == 0:
            return {
                "status": "error",
                "message": "Empty file",
                "file_name": file.filename
            }

        # Step 4: Corrupt image check
        try:
            img = Image.open(file_path)
            img.verify()
        except Exception:
            return {
                "status": "error",
                "message": "Corrupt image",
                "file_name": file.filename
            }

        # Step 5: Real analysis
        result = analyze_image(file_path)

        if not result:
            return {
                "status": "error",
                "message": "not found",
                "file_name": file.filename
            }

        # Step 6: Success response
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
    finally:
        file_path.unlink(missing_ok=True)
