import pandas as pd


def preprocess(filepath):
    """
    Loads only the columns required for analysis: date, product, total_sales.
    The dataset has more columns (category, region, salesperson, quantity,
    unit_price, discount) but we only load what we need.
    """
    df = pd.read_csv(filepath, usecols=["date", "product", "total_sales"])

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")

    df = df.dropna(subset=["date", "product", "total_sales"])
    df = df[df["total_sales"] > 0]
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")
    df = preprocess(data_path)
    print(f"Rows loaded : {len(df)}")
    print(f"Columns     : {list(df.columns)}")
    print()
    print(df.to_string())
