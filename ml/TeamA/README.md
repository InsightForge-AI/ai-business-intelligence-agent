# ml/TeamA — Sales Data Preprocessing

This module handles data cleaning and preprocessing for the sales dataset as part of the TeamA ML pipeline.

---

## Project Structure

```
ml/TeamA/
├── data/                   # Raw and processed datasets
│   └── sales_data.csv
├── notebooks/              # Jupyter notebooks for exploration
│   └── EDA.ipynb
├── src/                    # Core ML source code
│   ├── preprocessor.py
│   ├── model.py
│   ├── utils.py
│   └── __init__.py
├── tests/
│   └── test_preprocessor.py
├── requirements.txt
└── README.md
```

---

## What the Preprocessor Does

The `preprocess(filepath)` function in `src/preprocessor.py` accepts a raw CSV path and returns a cleaned DataFrame with four columns: `date`, `product`, `region`, `total_sales`.

Steps performed:
- Removes duplicate rows
- Standardizes text columns (`product`, `region`, `salesperson`, `category`) to Title Case
- Fills missing categorical values (`region`, `salesperson`) with the column mode
- Strips non-numeric characters from `unit_price` (e.g. `"55000 INR"` → `55000`)
- Fills missing numeric values with the column median
- Normalizes discount values entered as percentages (e.g. `15` → `0.15`)
- Drops rows where `quantity <= 0` or `total_sales <= 0`
- Parses `date` to datetime; drops rows with unparseable dates
- Retains only: `date`, `product`, `region`, `total_sales`

---

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest tests/test_preprocessor.py -v
```

## Usage

```python
from src.preprocessor import preprocess

df = preprocess("data/sales_data.csv")
print(df.head())
```
