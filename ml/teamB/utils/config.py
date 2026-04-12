from pathlib import Path


TEAM_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = TEAM_ROOT / "data"

API_TITLE = "ML Team B Analytics"
API_DESCRIPTION = "Sales data analysis service for Sprint 1 AI Business Intelligence."
API_VERSION = "1.0.0"
HOST = "127.0.0.1"
PORT = 8003

DATA_SOURCES = {
    "sales data": DATA_DIR / "sales_data.csv",
}

TREND_THRESHOLD = 0.05

ERROR_MESSAGES = {
    "file_not_found": "Data file not found",
    "processing_error": "Analysis failed",
    "insufficient_data": "No valid sales data available for analysis",
}