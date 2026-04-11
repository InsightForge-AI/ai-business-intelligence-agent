def get_insights(result):
    """
    Takes the analysis result dict and returns a plain-English insights summary.
    """
    total_sales = result["total_sales"]
    top_product = result["top_product"]
    trend = result["trend"]

    insights = (
        f"Total revenue stands at ₹{total_sales:,.2f}. "
        f"{top_product} is the best-performing product by sales. "
        f"Overall sales trend is {trend.lower()}."
    )

    return {"insights": insights}


if __name__ == "__main__":
    import os
    import sys
    from preprocess import preprocess
    from analysis import analyze

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")
    df = preprocess(data_path)
    result = analyze(df)
    output = get_insights(result)

    print("Insights:")
    print(f"  {output['insights']}")
