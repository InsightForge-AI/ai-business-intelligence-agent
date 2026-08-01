"""
==========================================================
Outlier Detection
==========================================================

Responsibilities
----------------
• Detect outliers using IQR
• Remove outliers
"""

from typing import Dict, List, Tuple

import pandas as pd


def get_numeric_columns(
    dataframe: pd.DataFrame
) -> List[str]:
    """
    Return numeric columns.
    """

    return dataframe.select_dtypes(
        include="number"
    ).columns.tolist()


def detect_outliers(
    dataframe: pd.DataFrame
) -> Dict:
    """
    Detect outliers using IQR.
    """

    numeric_columns = get_numeric_columns(
        dataframe
    )

    report = {}

    total = 0

    for column in numeric_columns:

        series = dataframe[column].dropna()

        if series.empty:

            report[column] = 0

            continue

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)

        upper = q3 + (1.5 * iqr)

        count = (

            (series < lower)

            |

            (series > upper)

        ).sum()

        report[column] = int(count)

        total += int(count)

    return {

        "total_outliers": total,

        "columns": report

    }


def remove_outliers(
    dataframe: pd.DataFrame
) -> Tuple[pd.DataFrame, Dict]:
    """
    Remove outliers.
    """

    numeric_columns = get_numeric_columns(
        dataframe
    )

    cleaned = dataframe.copy()

    report = {}

    for column in numeric_columns:

        series = cleaned[column]

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)

        upper = q3 + (1.5 * iqr)

        before = len(cleaned)

        cleaned = cleaned[

            (cleaned[column] >= lower)

            &

            (cleaned[column] <= upper)

        ]

        removed = before - len(cleaned)

        report[column] = removed

    cleaned.reset_index(
        drop=True,
        inplace=True
    )

    return cleaned, report