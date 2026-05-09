import json
import re


def build_prompt(query: str) -> str:
    return f"""You are a Senior Business Intelligence Consultant specialized in the Indian Retail Market.
The user is asking for analysis on: "{query}"

Task: Generate a realistic simulated analysis based on Indian market benchmarks.

The JSON must have exactly these keys:
- total_sales: a string in human-readable Indian terms (e.g., '₹1.5 Lakh Cr', '₹850 Cr', or '₹40 Lakh')
- top_product: a specific product model or sub-category
- trend: one of "increasing", "decreasing", or "stable"
- insights: exactly 3 short, punchy sentences.

Constraint: All monetary values in Indian Rupees (₹). Respond with raw JSON only. Do not exceed 120 words for insights."""


def get_insights(query: str, call_llm) -> dict:
    res = {
        "total_sales": None,
        "top_product": None,
        "trend": None,
        "error": None,
        "insights": None
    }

    response = call_llm("deepseek-r1:1.5b", build_prompt(query))

    if not response:
        res["error"] = "LLM unavailable or connection timeout"
        return res

    try:
        clean_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
        match = re.search(r"\{.*\}", clean_response, re.DOTALL)
        if match:
            data = json.loads(match.group())
            res["total_sales"] = data.get("total_sales", "₹0")
            res["top_product"] = data.get("top_product")
            res["trend"]       = data.get("trend")
            res["error"]       = None

            raw_insights = data.get("insights", "")
            if isinstance(raw_insights, list):
                raw_insights = " ".join(raw_insights)
            sentences = re.split(r'(?<=[.!?]) +', str(raw_insights).strip())
            res["insights"] = " ".join(sentences[:3])
        else:
            res["error"] = "Could not parse LLM JSON response"
    except Exception as e:
        res["error"] = f"Internal processing error: {str(e)}"

    return res