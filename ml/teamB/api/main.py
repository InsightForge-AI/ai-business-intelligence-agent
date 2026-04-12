from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ml.teamB.src.analysis import get_insights
from ml.teamB.src.preprocess import load_sales_data


TEAM_ROOT = Path(__file__).resolve().parents[1]
DATA_SOURCES = {
    "sales data": TEAM_ROOT / "data" / "sales_data.csv",
}

app = FastAPI(title="ML Team B Analytics", version="1.0.0")


class AnalyzeRequest(BaseModel):
    data: str
    filters: dict[str, Any] | None = None


@app.get("/health")
def health_check() -> dict[str, Any]:
    return {
        "status": "ok",
        "sprint": 1,
        "endpoint": "POST/ml/analyze",
        "available_data_sources": list(DATA_SOURCES.keys()),
    }


@app.post("/ml/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    source_name = request.data.strip().lower()
    file_path = DATA_SOURCES.get(source_name)

    if file_path is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown data source. Available: {list(DATA_SOURCES.keys())}",
        )

    sales_df = load_sales_data(file_path)
    if sales_df.empty:
        raise HTTPException(status_code=400, detail="No valid sales data available for analysis")

    return get_insights(sales_df)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ml.teamB.api.main:app", host="127.0.0.1", port=8003, reload=False)
