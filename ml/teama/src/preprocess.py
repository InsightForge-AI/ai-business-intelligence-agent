import pandas as pd

def preprocess(filepath):
    df = pd.read_csv(filepath, usecols=["date", "product", "total_sales"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    return df

if __name__ == "__main__":
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")
    df = preprocess(data_path)
    print(df)