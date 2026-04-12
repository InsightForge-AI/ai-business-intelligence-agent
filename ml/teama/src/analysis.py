def analyze(df):
    """
    Analyzes preprocessed sales data.
    Returns total_sales, top_product, and trend.
    """
    total_sales = round(float(df["total_sales"].sum()), 2)

    top_product = df.groupby("product")["total_sales"].sum().idxmax()

    df_sorted = df.sort_values("date").reset_index(drop=True)
    mid = len(df_sorted) // 2
    first_half_avg = df_sorted["total_sales"].iloc[:mid].mean()
    second_half_avg = df_sorted["total_sales"].iloc[mid:].mean()

    if second_half_avg > first_half_avg * 1.05:
        trend = "Increasing"
    elif second_half_avg < first_half_avg * 0.95:
        trend = "Decreasing"
    else:
        trend = "Stable"

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

    print("Analysis Result:")
    print(f"  total_sales : {result['total_sales']}")
    print(f"  top_product : {result['top_product']}")
    print(f"  trend       : {result['trend']}")
