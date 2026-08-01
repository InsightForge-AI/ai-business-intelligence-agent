"""
==========================================================
Statistics
==========================================================

Responsibilities
----------------
• Calculate descriptive statistics
• Handle missing values safely
• Support any numeric dataset
"""

import pandas as pd


def calculate_statistics(
    dataframe: pd.DataFrame
):
    """
    Calculate descriptive statistics for all numeric columns.
    """

    statistics = {}

    numeric = dataframe.select_dtypes(
        include="number"
    )

    if numeric.empty:
        return statistics

    for column in numeric.columns:

        series = numeric[column].dropna()

        if series.empty:
            continue

        statistics[column] = {

            # ------------------------------------------
            # Basic Information
            # ------------------------------------------

            "count": int(series.count()),

            "missing": int(
                dataframe[column].isna().sum()
            ),

            "sum": round(
                float(series.sum()),
                2
            ),

            # ------------------------------------------
            # Central Tendency
            # ------------------------------------------

            "average": round(
                float(series.mean()),
                2
            ),

            "median": round(
                float(series.median()),
                2
            ),

            "mode": round(
                float(series.mode().iloc[0]),
                2
            ) if not series.mode().empty else None,

            # ------------------------------------------
            # Dispersion
            # ------------------------------------------

            "minimum": round(
                float(series.min()),
                2
            ),

            "maximum": round(
                float(series.max()),
                2
            ),

            "range": round(
                float(series.max() - series.min()),
                2
            ),

            "std": round(
                float(series.std()),
                2
            ) if series.count() > 1 else 0.0,

            "variance": round(
                float(series.var()),
                2
            ) if series.count() > 1 else 0.0,

            # ------------------------------------------
            # Quartiles
            # ------------------------------------------

            "q1": round(
                float(series.quantile(0.25)),
                2
            ),

            "q3": round(
                float(series.quantile(0.75)),
                2
            ),

            "iqr": round(
                float(
                    series.quantile(0.75)
                    - series.quantile(0.25)
                ),
                2
            )

        }

    return statistics