def _rule_based(result):
    total    = result.get("total_sales_formatted") or f"₹{result.get('total_sales', 0):,}"
    product  = result.get("top_product") or "N/A"
    trend    = result.get("trend", "stable")
    rankings = result.get("rankings", [])

    parts = [f"Total sales is {total}. {product} is the top performing product."]
    if rankings:
        breakdown = ", ".join([f"{r['product']} {r['share']}%" for r in rankings])
        parts.append(f"Product breakdown: {breakdown}.")
    if trend == "increasing":
        parts.append("Sales are trending upward. Consider scaling top performers.")
    elif trend == "decreasing":
        parts.append("Sales are declining. Review pricing or marketing strategy.")
    else:
        parts.append("Sales are stable. Explore new markets to drive growth.")
    return " ".join(parts)


def get_insights(result, call_llm=None):
    if call_llm:
        rankings = result.get("rankings", [])
        breakdown = ", ".join([f"{r['product']} ({r['share']}% of sales)" for r in rankings])
        total = result.get("total_sales_formatted") or f"₹{result.get('total_sales', 0):,}"
        prompt = f"""You are a business analyst. Write exactly 2-3 sentences as a single plain paragraph. No bullet points, no dashes, no newlines, no markdown, no parenthetical notes. Cover: what the numbers show, what the trend means for the business, and one specific recommendation.

Data:
- Total sales: {total}
- Top product: {result.get('top_product')}
- Trend: {result.get('trend')}
- Product breakdown: {breakdown}

3 sentences, plain paragraph, no extra commentary."""
        response = call_llm(prompt)
        if response:
            return {"insights": response}
    return {"insights": _rule_based(result)}