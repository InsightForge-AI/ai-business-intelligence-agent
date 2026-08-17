from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..src.search import simple_search

app = FastAPI()


class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose declared Content-Length exceeds a cap.

    Nothing enforced a size limit before -- arbitrarily large query
    bodies were accepted with no pushback. Content-Length check only,
    same tradeoff noted in backend/main.py's copy of this middleware.
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


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "AI_Business_Intelligent_Agent Simple RAG API is running!"}


@app.post("/rag/query")
def rag_query(request: QueryRequest):

    query = request.query

    if not query or not query.strip():
        return {
            "content": [],
            "total_results": 0,
            "message": "empty query"
        }

    results = simple_search(query)

    if len(results) == 0:
        return {
            "query": query,
            "content": [],
            "total_results": 0,
            "message": "not found"
        }

    return {
        "query": query,
        "content": [r["text"] for r in results],
        "total_results": len(results)
    }