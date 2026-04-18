def get_insights(result):
    # Handle error or invalid states first
    if result.get("trend") in ["invalid", "no data"]:
        return {"insights": f"Analysis halted: {result.get('trend')}."}

    # Format the product name for the string
    product = result['top_product'] if result['top_product'] else "None"

    return {
        "insights": (
            f"Total sales is {result['total_sales']}. "
            f"{product} is the top performing product. "
            f"Sales trend is {result['trend']}."
        )
    }