import os, importlib.util
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

BASE = os.path.dirname(__file__)
SRC  = os.path.join(BASE, "..", "src")
LLM  = os.path.join(BASE, "..", "llm")

preprocess   = load("p", os.path.join(SRC, "preprocess.py")).preprocess
analyze      = load("a", os.path.join(SRC, "analysis.py")).analyze
get_insights = load("i", os.path.join(SRC, "insights.py")).get_insights
call_llm     = load("l", os.path.join(LLM, "llm.py")).call_llm

app = FastAPI()

class SalesRequest(BaseModel):
    data: Union[str, dict, list]

@app.post("/ml/analyze")
def ml_analyze(req: SalesRequest):
    if isinstance(req.data, str) and not req.data.endswith(".csv"):
        filepath = os.path.join(BASE, "..", "data", "sales_data.csv")
        df, col_map = preprocess(filepath)
    else:
        df, col_map = preprocess(req.data)

    res = analyze(df, col_map)
    res.update(get_insights(res, call_llm=call_llm))
    res.pop("rankings", None)
    res["total_sales"] = res.pop("total_sales_formatted", f"₹{res['total_sales']:,}")
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)