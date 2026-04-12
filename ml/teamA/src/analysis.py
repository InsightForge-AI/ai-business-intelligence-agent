def analyze(df):
    total_sales = int(df["total_sales"].sum())
    top_product = df.loc[df["total_sales"].idxmax(), "product"]
    trend = "Increasing" if df["total_sales"].iloc[-1] > df["total_sales"].iloc[0] else "Decreasing"

    return {
        "total_sales": total_sales,
        "top_product": top_product,
        "trend": trend,
    }

if __name__ == "__main__":
    import os
    from preprocess import preprocess

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")
    df = preprocess(data_path)
    result = analyze(df)
    print(result)
