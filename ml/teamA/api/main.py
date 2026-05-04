import os, importlib.util
from fastapi import FastAPI
from pydantic import BaseModel

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

BASE = os.path.dirname(__file__)
SRC  = os.path.join(BASE, "..", "src")
LLM  = os.path.join(BASE, "..", "llm")

analyze  = load("a", os.path.join(SRC, "analysis.py")).analyze
call_llm = load("l", os.path.join(LLM, "llm.py")).call_llm

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ml/analyze")
def ml_analyze(req: QueryRequest):
    return analyze(req.query, call_llm)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)