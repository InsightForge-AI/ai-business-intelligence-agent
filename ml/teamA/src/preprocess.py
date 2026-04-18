import pandas as pd

def preprocess(filepath):
    try:
        # Case 2: Read file; handling possible empty file or missing headers
        df = pd.read_csv(filepath)
        
        # Case 8: Ensure the 'product' column exists
        if "product" not in df.columns:
            df["product"] = "unknown"
            
        # Case 3 & 7: Ensure 'total_sales' column exists for numeric conversion later
        if "total_sales" not in df.columns:
            df["total_sales"] = None
            
        return df
    except Exception:
        # Return empty DataFrame so analysis.py knows no data was found
        return pd.DataFrame()