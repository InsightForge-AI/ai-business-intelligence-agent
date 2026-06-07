import json


def build_prompt(data_summary: dict, query: str) -> str:
    return f"""You are an expert business data analyst. You have been given a structured data summary computed from a business dataset and a user question.

The summary contains:
- Column names and data types
- Row count
- Null counts per column (only columns with nulls)
- Numeric totals per column
- Formatted totals in Indian currency (₹ Cr/Lakh/K)
- Outlier counts per numeric column
- Growth percentage between first and last time period (null if no date column)
- Group-wise totals for all categorical columns
- Sample rows

---

DATA SUMMARY:
{json.dumps(data_summary, indent=2)}

---

USER QUESTION:
"{query}"

---

Your tasks:
1. Read the user question and identify the key entity or dimension being asked about
2. From group_totals, find the grouping that best matches that entity or dimension
3. Use that grouping to identify top and bottom performers internally — do NOT include them in output
4. Use growth from the summary if available, otherwise derive trend from group totals
5. Identify revenue and profit from the totals — use the most relevant numeric columns
6. Generate one meaningful business insight using Indian currency formatting (₹ Cr/Lakh/K)
7. Answer the user question directly in 2-3 sentences using Indian currency formatting
8. Provide one actionable recommendation

Important rules:
- Do NOT make up numbers — use only what is in the data summary
- Do NOT assume column names — derive everything from what you see
- Use ₹ Cr/Lakh/K formatting only in insight, llm_answer and recommendation text
- KPI values must be plain numbers only
- top_performer, bottom_performer and growth are for your internal reasoning only — do NOT include them in the output JSON

Respond with ONLY a raw JSON object. No explanation. No markdown. No preamble.

{{
  "kpis": {{
    "revenue": <single total number>,
    "profit": <single total number>
  }},
  "trend": "<increasing | decreasing | stable>",
  "insight": "<one meaningful business insight using ₹ formatting>",
  "llm_answer": "<direct answer to user question in 2-3 sentences using ₹ formatting>",
  "recommendation": "<one actionable recommendation>"
}}"""