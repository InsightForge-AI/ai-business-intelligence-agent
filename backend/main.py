from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.logging_config import setup_logging

# start logging first
setup_logging()

from app.api.analyze import router


app = FastAPI(
    title="Backend Team",
    description="Integration Layer",
    version="1.0"
)


class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose declared Content-Length exceeds a cap.

    Nothing enforced a size limit before, so a large text body or a
    base64-encoded image (which run ~33% larger than the raw file) could
    grow unbounded. This is a Content-Length check, not a streaming
    enforcement -- a client that lies about its own header can still send
    more, but it stops the common case cheaply, before the body is read.
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


# 15MB accommodates a ~10MB image re-encoded as base64 (~33% larger) inside
# the JSON body sent to /analyze.
app.add_middleware(MaxBodySizeMiddleware, max_bytes=15 * 1024 * 1024)


# allow_origins is intentionally an explicit list, not "*": this API is
# public (no auth), and combining a wildcard origin with
# allow_credentials=True makes Starlette reflect back *any* request
# Origin verbatim with credentials allowed -- effectively no CORS
# protection at all. Nothing here relies on cookies/session credentials,
# so allow_credentials is off and only the frontend's own known origins
# are trusted.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def home():
    return {"status": "Backend running"}