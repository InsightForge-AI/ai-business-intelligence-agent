from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from ml.teamA.src.analysis import analyze
from ml.teamA.llm.llm_service import call_llm


app = FastAPI()


class QueryRequest(BaseModel):
    query: Optional[str] = None
    data: Optional[str] = None


@app.post("/ml/analyze")
def ml_analyze(req: QueryRequest):

    user_input = req.query or req.data

    if not user_input:
        return {
            "error": "Please provide either 'query' or 'data'"
        }

    return analyze(user_input, call_llm)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ml.teamA.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )