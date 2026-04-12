def get_insights(result):
    return {
        "insights": (
            f"Total sales is {result['total_sales']}. "
            f"{result['top_product']} is the top performing product. "
            f"Sales trend is {result['trend']}."
        )
    }

if __name__ == "__main__":
    import os
    from preprocess import preprocess
    from analysis import analyze

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")
    df = preprocess(data_path)
    result = analyze(df)
    print(get_insights(result))
