import json
import re


def build_prompt(query: str) -> str:
    return f"""You are a business analyst. Answer this query: "{query}"

Reply with only a JSON object with these keys:
- total_sales: estimated sales in Indian Rupees using proper Indian business number formatting like ₹ symbol and Cr or Lakh Cr format
- top_product: a specific product name with brand and model, not just the brand name
- trend: one of increasing, decreasing, or stable
- insights: maximum 2 sentences covering what the data shows and one recommendation

Raw JSON only. No explanation. No markdown."""


def get_insights(query: str, call_llm) -> dict:

    result = {
        "total_sales": None,
        "top_product": None,
        "trend": None,
        "error": None,
        "insights": None
    }

    llm_response = call_llm(
        "deepseek-r1:1.5b",
        build_prompt(query)
    )

    if not llm_response:
        result["error"] = "LLM unavailable or connection timeout"
        return result

    try:

        cleaned_response = re.sub(
            r"<think>.*?</think>",
            "",
            llm_response,
            flags=re.DOTALL
        ).strip()

        json_match = re.search(
            r"\{.*\}",
            cleaned_response,
            re.DOTALL
        )

        if not json_match:
            result["error"] = "Could not parse LLM JSON response"
            return result

        parsed_data = json.loads(json_match.group())

        result["total_sales"] = parsed_data.get("total_sales", "₹0")
        result["top_product"] = parsed_data.get("top_product")
        result["trend"] = parsed_data.get("trend")

        raw_insights = parsed_data.get("insights", "")

        if isinstance(raw_insights, list):
            raw_insights = " ".join(raw_insights)

        sentences = re.split(
            r'(?<=[.!?]) +',
            str(raw_insights).strip()
        )

        result["insights"] = " ".join(sentences[:2])

    except Exception as e:
        result["error"] = f"Internal processing error: {str(e)}"

    return result
