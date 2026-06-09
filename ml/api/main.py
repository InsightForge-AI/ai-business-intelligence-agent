from fastapi import FastAPI
from pydantic import BaseModel

from ml.analysis.analysis import analyze


app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/ml/analyze")
def ml_analyze(req: QueryRequest):

    if not req.query or not req.query.strip():
        return {"error": "Please provide a query"}

    return analyze(req.query.strip())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)