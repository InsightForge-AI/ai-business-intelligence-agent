import pandas as pd

def analyze(df):
    res = {"total_sales": 0, "top_product": "null", "trend": "invalid", "error": None}

    try:
        if df.empty:
            res.update({"top_product": None, "trend": "no data"})
            return res

        sales_series = pd.to_numeric(df["total_sales"], errors='coerce')
        has_nans = sales_series.isna().any()
        
        # Fill NaNs with 0 for calculations
        clean_sales = sales_series.fillna(0)
        total = clean_sales.sum()
        
        res["total_sales"] = float(total) if total % 1 else int(total)

        if total == 0 and not has_nans:
            res["top_product"] = None
            res["trend"] = "no trend"
        elif total == 0 and has_nans:
            res["top_product"] = "null"
            res["trend"] = "invalid"
        else:
            res["top_product"] = df.loc[clean_sales.idxmax(), "product"]
            
            first, last = clean_sales.iloc[0], clean_sales.iloc[-1]
            
            if has_nans:
                res["trend"] = "partial"
            elif len(df) == 1:
                res["trend"] = "stable" 
            elif last > first:
                res["trend"] = "increasing"
            elif last < first:
                res["trend"] = "decreasing"
            else:
                res["trend"] = "stable"

    except Exception as e:
        res["trend"] = "invalid"
        res["error"] = str(e)

    return res
