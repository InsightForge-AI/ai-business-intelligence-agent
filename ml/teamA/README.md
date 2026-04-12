# Team A — Sales Analytics

A lightweight sales analytics service that reads sales data, processes it, and returns business insights through a REST API.

---

## Project Structure

```
ml/
└── teama/
    ├── README.md
    ├── requirements.txt
    ├── api/
    │   ├── __init__.py
    │   └── main.py          # FastAPI app — defines POST /ml/analyze
    ├── src/
    │   ├── __init__.py
    │   ├── preprocess.py    # Loads only required columns, cleans data
    │   ├── analysis.py      # Computes total_sales, top_product, trend
    │   └── insights.py      # Generates plain-English insights from analysis
    └── data/
        └── sales_data.csv   # 100-row clean sales dataset
```

---

## What Each File Does

| File | Role |
|------|------|
| `api/main.py` | FastAPI entry point. Accepts a POST request, runs the full pipeline, returns JSON |
| `src/preprocess.py` | Reads the CSV, loads only the 3 required columns, cleans types and nulls |
| `src/analysis.py` | Takes the cleaned dataframe, computes total sales, top product, and sales trend |
| `src/insights.py` | Takes the analysis result and returns a human-readable summary string |
| `data/sales_data.csv` | Source dataset with 100 records across 9 columns |

---

## Setup

Make sure you are in the `teama/` directory, then install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Server

```bash
# From inside ml/teama/api/
python main.py
```

The server starts at `http://localhost:8000`.

---

## API Reference

### POST `/ml/analyze`

Runs the full pipeline — preprocess → analyze → insights — and returns the result.

**Request Body**
```json
{
  "data": "sales data"
}
```

**Response**
```json
{
  "total_sales": 1945130.96,
  "top_product": "Laptop",
  "trend": "Increasing",
  "insights": "Total revenue stands at ₹1,945,130.96. Laptop is the best-performing product by sales. Overall sales trend is increasing."
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `total_sales` | float | Sum of all sales values in the dataset |
| `top_product` | string | Product with the highest total revenue |
| `trend` | string | `Increasing`, `Decreasing`, or `Stable` — based on first vs second half average |
| `insights` | string | Plain-English summary of the above three fields |

---

## Dataset

**File:** `data/sales_data.csv`
**Records:** 100 rows, 9 columns

| Column | Description |
|--------|-------------|
| `date` | Transaction date (DD-MM-YYYY) |
| `product` | Product name |
| `category` | Product category (Electronics, Accessories, Wearables) |
| `region` | Sales region (North, South, East, West) |
| `salesperson` | Name of the salesperson |
| `quantity` | Number of units sold |
| `unit_price` | Price per unit in INR |
| `discount` | Discount applied (0.0, 0.05, 0.10, or 0.15) |
| `total_sales` | Final sale value after discount |

> **Note:** `preprocess.py` intentionally loads only `date`, `product`, and `total_sales` — the other columns exist in the dataset for reference but are not required for Sprint 1 analysis.

---

## How the Pipeline Works

```
Request → preprocess() → analyze() → get_insights() → Response
```

1. `preprocess()` — reads the CSV, selects the 3 needed columns, converts types, drops nulls and negative values
2. `analyze()` — calculates total sales, finds the top product, determines trend by comparing the average of the first half of records vs the second half (sorted by date)
3. `get_insights()` — wraps the numeric results into a readable sentence

---

## Sprint 1 Rules Followed

- Simple processing only — no advanced preprocessing
- No external API calls
- No extra fields in the output beyond what is specified
- Dataset is clean and minimal
