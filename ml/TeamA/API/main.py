import os
import sys

# --- AUTOMATIC ROOT DISCOVERY ---
# This looks 3 levels up from this file (API -> TeamA -> ml -> Root)
# and adds it to the Python path so "from ml.TeamA..." works everywhere.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# imports from src folder
from ml.TeamA.src.preprocessor import preprocess
from ml.TeamA.src.analysis import analyze
from ml.TeamA.src.insights import get_final_report

app = FastAPI(title="Sales Analytics API")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Keyword to file path mapping
DATA_SOURCES = {
    "sales data": os.path.join(BASE_DIR, "data", "sales_data.csv")
}

# Request schema
class SalesDataRequest(BaseModel):
    data: str

@app.post("/ml/analyze")
async def ml_analyze(request: SalesDataRequest):
    """
    Accepts a keyword in the 'data' field and maps it to the actual CSV file.
    Example input: { "data": "sales data" }
    """
    try:
        # Step 1: Resolve keyword → file path
        source = DATA_SOURCES.get(request.data.lower().strip())

        if not source:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown data source: '{request.data}'. Available sources: {list(DATA_SOURCES.keys())}"
            )

        # Step 2: Preprocess data
        df = preprocess(source)

        if df is None or df.empty:
            raise HTTPException(
                status_code=400,
                detail="Dataset is empty after preprocessing."
            )

        # Step 3: Analyze data
        analysis_results = analyze(df)

        # Step 4: Generate final report
        final_report = get_final_report(df, analysis_results)

        return final_report

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"CSV file not found at: {source}"
        )

    except Exception as e:
        print(f"Error details: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # We use the string import so 'reload=True' works correctly
    uvicorn.run("ml.TeamA.API.main:app", host="127.0.0.1", port=8000, reload=True)