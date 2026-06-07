import json
import re
import pandas as pd

from ml.teamA.llm.llm_service import call_llm
from ml.teamA.prompts.prompts import build_prompt


HARDCODED_FILE_PATH = "ml/teamA/tests/sample_sales.csv"


def format_indian(value: float) -> str:
    """Format number in Indian currency style."""
    if value >= 1_00_00_000:
        return f"₹{value / 1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:
        return f"₹{value / 1_00_000:.2f} Lakh"
    elif value >= 1_000:
        return f"₹{value / 1_000:.2f} K"
    else:
        return f"₹{value:.2f}"


def compute_growth(df: pd.DataFrame, numeric_cols: list) -> str | None:
    """Detect date column and compute growth between first and last period."""

    date_col = None

    for col in df.columns:
        if df[col].dtype == "object":
            try:
                parsed = pd.to_datetime(df[col], infer_datetime_format=True)
                if parsed.notna().sum() > len(df) * 0.8:
                    date_col = col
                    df[col] = parsed
                    break
            except Exception:
                continue

    if date_col is None:
        return None

    df["_period"] = df[date_col].dt.to_period("M")
    periods = sorted(df["_period"].unique())

    if len(periods) < 2:
        return None

    first_period = df[df["_period"] == periods[0]][numeric_cols].sum().sum()
    last_period = df[df["_period"] == periods[-1]][numeric_cols].sum().sum()

    if first_period == 0:
        return None

    growth = ((last_period - first_period) / first_period) * 100

    return f"{'+' if growth >= 0 else ''}{growth:.1f}%"


def remove_outliers(df: pd.DataFrame, numeric_cols: list) -> tuple[pd.DataFrame, dict]:
    """Remove outlier rows using IQR method and return cleaned df and outlier report."""

    outliers = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR

        flagged = df[df[col] > upper_bound]
        if len(flagged) > 0:
            outliers[col] = int(len(flagged))
            df = df[df[col] <= upper_bound]

    return df, outliers


def load_and_summarize(file_path: str) -> dict:
    """Load file and extract clean focused stats using pandas."""

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel allowed.")

    summary = {}

    # Structure
    summary["columns"] = list(df.columns)
    summary["row_count"] = int(len(df))

    # Null counts — only columns that actually have nulls
    null_counts = df.isnull().sum()
    summary["null_counts"] = {col: int(v) for col, v in null_counts.items() if v > 0}

    # Numeric cols
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Removing outliers using IQR
    df, outliers = remove_outliers(df, numeric_cols)
    summary["outliers_removed"] = outliers
    summary["clean_row_count"] = int(len(df))
    summary["totals"] = {col: float(df[col].sum()) for col in numeric_cols}
    summary["formatted_totals"] = {col: format_indian(float(df[col].sum())) for col in numeric_cols}
    summary["growth"] = compute_growth(df.copy(), numeric_cols)

    # Group totals from clean data
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    summary["group_totals"] = {}

    for cat_col in categorical_cols:
        group = df.groupby(cat_col)[numeric_cols].sum().round(2)
        summary["group_totals"][cat_col] = json.loads(group.to_json())

    summary["sample_rows"] = json.loads(df.head(3).fillna("").to_json(orient="records"))

    return summary


def analyze(query: str) -> dict:
    """Load file, summarize with pandas, call LLM, return structured result."""

    result = {
        "kpis": {
            "revenue": None,
            "profit": None
        },
        "trend": None,
        "insight": None,
        "llm_answer": None,
        "recommendation": None,
        "error": None
    }

    try:
        data_summary = load_and_summarize(HARDCODED_FILE_PATH)
    except FileNotFoundError:
        result["error"] = f"File not found. Please ensure the file is available."
        return result
    except Exception as e:
        result["error"] = f"Failed to read file: {str(e)}"
        return result

    prompt = build_prompt(data_summary, query)

    llm_response = call_llm("deepseek-r1:7b", prompt)

    if not llm_response:
        result["error"] = "LLM unavailable or connection timeout"
        return result

    cleaned_response = re.sub(
        r"<think>.*?</think>",
        "",
        llm_response,
        flags=re.DOTALL
    ).strip()


    cleaned_response = re.sub(r",\s*([}\]])", r"\1", cleaned_response)

    # Extract JSON
    json_match = re.search(
        r"\{.*\}",
        cleaned_response,
        re.DOTALL
    )

    if not json_match:
        result["error"] = "Could not parse LLM JSON response"
        return result

    try:
        parsed = json.loads(json_match.group())

        kpis = parsed.get("kpis", result["kpis"])

        # KPI values in Indian currency
        if kpis.get("revenue"):
            kpis["revenue"] = format_indian(float(kpis["revenue"]))
        if kpis.get("profit"):
            kpis["profit"] = format_indian(float(kpis["profit"]))

        result["kpis"] = kpis
        result["trend"] = parsed.get("trend")
        result["insight"] = parsed.get("insight")
        result["llm_answer"] = parsed.get("llm_answer")
        result["recommendation"] = parsed.get("recommendation")

    except Exception as e:
        result["error"] = f"Internal processing error: {str(e)}"

    return result