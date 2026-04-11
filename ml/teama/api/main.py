import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from ..src.preprocess import preprocess
    from ..src.analysis import analyze
    from ..src.insights import get_insights
except ImportError:
    import importlib.util

    def _load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    _src = os.path.join(os.path.dirname(__file__), "..", "src")
    preprocess = _load("preprocess", os.path.join(_src, "preprocess.py")).preprocess
    analyze    = _load("analysis",   os.path.join(_src, "analysis.py")).analyze
    get_insights = _load("insights", os.path.join(_src, "insights.py")).get_insights

app = FastAPI(title="Sales Analytics API - Team A")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")


class SalesRequest(BaseModel):
    data: str


@app.post("/ml/analyze")
async def ml_analyze(request: SalesRequest):
    if request.data.lower().strip() != "sales data":
        raise HTTPException(
            status_code=400,
            detail=f"Unknown data source: '{request.data}'. Use: 'sales data'"
        )

    try:
        df = preprocess(DATA_PATH)

        if df.empty:
            raise HTTPException(status_code=400, detail="Dataset is empty after loading.")

        result = analyze(df)
        result.update(get_insights(result))
        return result

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="sales_data.csv not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
