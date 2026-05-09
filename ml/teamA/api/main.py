import os, importlib.util
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

BASE = os.path.dirname(__file__)
SRC  = os.path.join(BASE, "..", "src")
LLM  = os.path.join(BASE, "..", "llm")

analyze  = load("a", os.path.join(SRC, "analysis.py")).analyze
call_llm = load("l", os.path.join(LLM, "llm_service.py")).call_llm

app = FastAPI()

class QueryRequest(BaseModel):
    query: Optional[str] = None
    data: Optional[str] = None

@app.post("/ml/analyze")
def ml_analyze(req: QueryRequest):
    user_input = req.query or req.data
    if not user_input:
        return {"error": "Please provide either 'query' or 'data' field"}
    return analyze(user_input, call_llm)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
