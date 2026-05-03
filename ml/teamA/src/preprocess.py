import pandas as pd

CATEGORY_HINTS = ["product", "category", "region", "department", "name", "item", "type", "brand"]
DATE_HINTS     = ["date", "time", "month", "year", "period", "day", "week"]


def detect_columns(df):
    col_map = {"numeric": None, "category": None, "date": None}
    
    # Priority order for numeric — more specific beats generic
    NUMERIC_PRIORITY = ["total_sales", "total", "sales", "revenue", "amount", "price", "profit", "cost", "value", "quantity"]
    
    for col in df.columns:
        c = col.lower()
        if not col_map["date"] and any(h in c for h in DATE_HINTS):
            try:
                pd.to_datetime(df[col], dayfirst=True, errors="raise")
                col_map["date"] = col
            except: pass
        elif not col_map["category"] and any(h in c for h in CATEGORY_HINTS):
            if df[col].dtype == object:
                col_map["category"] = col

    # For numeric — pick highest priority match across all columns
    for hint in NUMERIC_PRIORITY:
        for col in df.columns:
            if hint in col.lower() and pd.to_numeric(df[col], errors="coerce").notna().sum() > 0:
                col_map["numeric"] = col
                break
        if col_map["numeric"]:
            break

    return col_map

def preprocess(data):
    try:
        if isinstance(data, str):
            df = pd.read_csv(data)
            for col in df.columns:
                if any(h in col.lower() for h in DATE_HINTS):
                    try: df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
                    except: pass
        elif isinstance(data, dict):
            df = pd.DataFrame(list(data.items()), columns=["category", "value"])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            return pd.DataFrame(), {}
        return df, detect_columns(df)
    except:
        return pd.DataFrame(), {}