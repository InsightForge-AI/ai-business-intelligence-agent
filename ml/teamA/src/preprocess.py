import pandas as pd

def preprocess(filepath):
    try:
        df = pd.read_csv(filepath)
        
        # Case 8: Ensure the 'product' column exists
        if "product" not in df.columns:
            df["product"] = "unknown"
            
        if "total_sales" not in df.columns:
            df["total_sales"] = None
            
        return df
    except Exception:
        return pd.DataFrame()
