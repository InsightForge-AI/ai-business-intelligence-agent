"""
==========================================================
Trend Analysis
==========================================================

Responsibilities
----------------
• Detect dataset type
• Analyze time-based trends
• Analyze category-wise trends
• Analyze numeric trends
• Generic fallback analysis
"""

import pandas as pd

from analysis.kpi import (
    find_column,
    SALES_COLUMNS,
    PROFIT_COLUMNS
)


TIME_COLUMNS = [
    "Date",
    "Year",
    "Month",
    "Quarter"
]


# ==========================================================
# Dataset Detection
# ==========================================================

def detect_dataset_type(df: pd.DataFrame):

    cols = {
        c.lower()
        for c in df.columns
    }

    if (
        "product" in cols and
        any(col in cols for col in map(str.lower, SALES_COLUMNS))
    ):
        return "retail"

    if (
        "department" in cols and
        "bill" in cols
    ):
        return "hospital"

    if (
        "salary" in cols or
        "employee" in cols
    ):
        return "hr"

    if (
        "expense" in cols or
        "income" in cols
    ):
        return "finance"

    return "generic"


# ==========================================================
# Retail Trends
# ==========================================================

def retail_trends(df):

    trends = {}

    time = find_column(
        df,
        TIME_COLUMNS
    )

    sales = find_column(
        df,
        SALES_COLUMNS
    )

    profit = find_column(
        df,
        PROFIT_COLUMNS
    )

    if time and sales:

        grouped = (
            df
            .groupby(time)[sales]
            .sum()
        )

        trends["sales_trend"] = {

            str(k): float(v)

            for k, v in grouped.items()

        }

    if time and profit:

        grouped = (
            df
            .groupby(time)[profit]
            .sum()
        )

        trends["profit_trend"] = {

            str(k): float(v)

            for k, v in grouped.items()

        }

    return trends


# ==========================================================
# Hospital Trends
# ==========================================================

def hospital_trends(df):

    trends = {}

    if (
        "Department" in df.columns and
        "Bill" in df.columns
    ):

        avg_bill = (

            df

            .groupby("Department")["Bill"]

            .mean()

            .round(2)

        )

        trends["average_bill"] = {

            k: float(v)

            for k, v in avg_bill.items()

        }

    if (

        "Department" in df.columns and

        "DaysAdmitted" in df.columns

    ):

        stay = (

            df

            .groupby("Department")["DaysAdmitted"]

            .mean()

            .round(2)

        )

        trends["average_stay"] = {

            k: float(v)

            for k, v in stay.items()

        }

    return trends


# ==========================================================
# HR Trends
# ==========================================================

def hr_trends(df):

    trends = {}

    if (

        "Department" in df.columns and

        "Salary" in df.columns

    ):

        grouped = (

            df

            .groupby("Department")["Salary"]

            .mean()

            .round(2)

        )

        trends["department_salary"] = {

            k: float(v)

            for k, v in grouped.items()

        }

    return trends


# ==========================================================
# Finance Trends
# ==========================================================

def finance_trends(df):

    trends = {}

    numeric = df.select_dtypes(
        include="number"
    )

    for column in numeric.columns:

        series = numeric[column]

        trends[column] = {

            "average": float(series.mean()),

            "minimum": float(series.min()),

            "maximum": float(series.max())

        }

    return trends


# ==========================================================
# Generic Trends
# ==========================================================

def generic_trends(df):

    trends = {}

    numeric = df.select_dtypes(
        include="number"
    )

    categorical = df.select_dtypes(
        exclude="number"
    )

    # Numeric summaries

    for column in numeric.columns:

        series = numeric[column]

        trends[column] = {

            "average": float(series.mean()),

            "minimum": float(series.min()),

            "maximum": float(series.max()),

            "median": float(series.median())

        }

    # Category distributions

    for column in categorical.columns[:3]:

        counts = (

            df[column]

            .value_counts()

            .head(10)

        )

        trends[f"{column}_distribution"] = {

            str(k): int(v)

            for k, v in counts.items()

        }

    return trends


# ==========================================================
# Main Entry
# ==========================================================

def analyze_trends(
    dataframe: pd.DataFrame
):

    dataset = detect_dataset_type(
        dataframe
    )

    if dataset == "retail":

        return retail_trends(
            dataframe
        )

    if dataset == "hospital":

        return hospital_trends(
            dataframe
        )

    if dataset == "hr":

        return hr_trends(
            dataframe
        )

    if dataset == "finance":

        return finance_trends(
            dataframe
        )

    return generic_trends(
        dataframe
    )