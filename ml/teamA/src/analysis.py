import pandas as pd

def analyze(df):
    # Default structure matching your Expected Output Format
    res = {"total_sales": 0, "top_product": "null", "trend": "invalid", "error": None}

    try:
        # Case 2: Empty Dataset
        if df.empty:
            res.update({"top_product": None, "trend": "no data"})
            return res

        # Case 7 & 9: Safe conversion (Wrong Datatypes/Strings become NaN)
        # We keep a copy to check for Case 3 (Missing Values)
        sales_series = pd.to_numeric(df["total_sales"], errors='coerce')
        has_nans = sales_series.isna().any()
        
        # Fill NaNs with 0 for calculations
        clean_sales = sales_series.fillna(0)
        total = clean_sales.sum()
        
        # Formatting total_sales (Normalizes decimals for Case 6)
        res["total_sales"] = float(total) if total % 1 else int(total)

        # Case 4 & 9: Top Product logic
        if total == 0 and not has_nans:
            res["top_product"] = None
            res["trend"] = "no trend"
        elif total == 0 and has_nans:
            res["top_product"] = "null"
            res["trend"] = "invalid"
        else:
            # Case 1, 6, 10: Standard analysis
            res["top_product"] = df.loc[clean_sales.idxmax(), "product"]
            
            # Trend Logic (Case 1, 3, 5, 11, 12)
            first, last = clean_sales.iloc[0], clean_sales.iloc[-1]
            
            if has_nans:
                res["trend"] = "partial" # Case 3
            elif len(df) == 1:
                res["trend"] = "stable"  # Case 11
            elif last > first:
                res["trend"] = "increasing" # Case 1
            elif last < first:
                res["trend"] = "decreasing" # Case 5
            else:
                res["trend"] = "stable"  # Case 12

    except Exception as e:
        res["trend"] = "invalid"
        res["error"] = str(e)

    return res