# ML Team B Sprint 1 Service

## Overview

ML Team B follows a simplified Sprint 1 workflow aligned with the backend team's expectation. The service keeps a small structure, uses one local sales dataset, and exposes one main API contract for analytics.

## Project Structure

```text
ml/teamB/
├── api/
│   ├── __init__.py
│   └── main.py
├── src/
│   ├── __init__.py
│   ├── preprocess.py
│   └── analysis.py
├── data/
│   └── sales_data.csv
├── requirements.txt
└── README.md
```

## API Contract

### Health Check

- `GET /health`

Example response:

```json
{
  "status": "ok",
  "sprint": 1,
  "endpoint": "POST /ml/analyze",
  "available_data_sources": ["sales data"]
}
```

### Sales Analysis

- `POST /ml/analyze`

Request:

```json
{
  "data": "sales data"
}
```

Response:

```json
{
  "total_sales": 12345.67,
  "top_product": "Science",
  "trend": "increasing",
  "insights": "Processed valid rows and generated simple Sprint 1 business insights."
}
```

## Workflow

- `src/preprocess.py` loads and cleans the sales CSV
- `src/analysis.py` computes total sales, top product, trend, and insights
- `api/main.py` exposes the FastAPI endpoints

## Run From Repository Root

```bash
python -m uvicorn ml.teamB.api.main:app --host 127.0.0.1 --port 8003 --reload
```

## Sprint 1 Notes

- Advanced filters are out of scope for this simplified version
- The request still accepts `{"data": "sales data"}` for compatibility
- The response keeps `insights` to preserve Team B output expectations
