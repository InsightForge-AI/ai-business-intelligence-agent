import os, importlib.util
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Union

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

BASE = os.path.dirname(__file__)
SRC = os.path.join(BASE, "..", "src")

preprocess = load("p", os.path.join(SRC, "preprocess.py")).preprocess
analyze = load("a", os.path.join(SRC, "analysis.py")).analyze
get_insights = load("i", os.path.join(SRC, "insights.py")).get_insights

app = FastAPI()


class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose declared Content-Length exceeds a cap.

    Nothing enforced a size limit before. Content-Length check only, same
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

class SalesRequest(BaseModel):
    data: Union[str, dict[str, float]]

@app.post("/ml/analyze")
def ml_analyze(req: SalesRequest):
    # Option 1: User sends "sales data" (String)
    if isinstance(req.data, str):
        filepath = os.path.join(BASE, "..", "data", "sales_data.csv")
        df = preprocess(filepath)
    
    else:
        df = pd.DataFrame(list(req.data.items()), columns=["product", "total_sales"])

    res = analyze(df)
    res.update(get_insights(res))
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)