from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..src.sentiment import get_sentiment
from ..src.keywords import get_keywords
from ..src.summarizer import summarize

app = FastAPI()


class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose declared Content-Length exceeds a cap.

    Nothing enforced a size limit before -- arbitrarily large text bodies
    were accepted with no pushback. Content-Length check only, same
    tradeoff noted in backend/main.py's copy of this middleware.
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


app.add_middleware(MaxBodySizeMiddleware, max_bytes=2 * 1024 * 1024)


@app.post("/nlp/analyze")
def analyze_text(data: dict):

    try:

        text = data.get("text", "")

        sentiment_result = get_sentiment(text)

        keywords_result = get_keywords(text)

        summary_result = summarize(text)

        return {
            "sentiment": sentiment_result,
            "summary": summary_result,
            "keywords": keywords_result,
        }

    except Exception as e:
        import logging
        logging.error(f"Error during NLP analysis: {e}", exc_info=True)

        # fallback response (never crash)

        return {
            "sentiment": "neutral",
            "summary": "processing error",
            "keywords": [],
        }