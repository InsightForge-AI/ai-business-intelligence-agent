import os, importlib.util
from fastapi import FastAPI
from pydantic import BaseModel


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


class SalesRequest(BaseModel):
    data: str


@app.post("/ml/analyze")
async def ml_analyze(req: SalesRequest):
    if req.data.lower().strip() != "sales data":
        return {"error": f"Unknown data source: '{req.data}'"}

    df = preprocess(os.path.join(BASE, "..", "data", "sales_data.csv"))

    if df.empty:
        return {"error": "Dataset is empty"}

    res = analyze(df)
    res.update(get_insights(res))
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)