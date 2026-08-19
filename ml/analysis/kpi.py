"""
==========================================================
Business KPI Calculator
==========================================================

Responsibilities
----------------
• Detect business columns
• Calculate KPIs
"""

import pandas as pd


SALES_COLUMNS = [
    "Sales",
    "Revenue",
    "Turnover",
    "Income"
]

PROFIT_COLUMNS = [
    "Profit",
    "Net Profit",
    "Gross Profit"
]

EXPENSE_COLUMNS = [
    "Expenses",
    "Cost",
    "Operating Cost"
]


def find_column(dataframe: pd.DataFrame, aliases: list[str]):
    """
    Return first matching column.
    """

    for column in dataframe.columns:

        if column.lower() in [

            alias.lower()

            for alias in aliases

        ]:

            return column

    return None


def calculate_kpis(
    dataframe: pd.DataFrame
) -> dict:
    """
    Calculate business KPIs.
    """

    kpis = {

        "rows": len(dataframe),

        "columns": len(dataframe.columns)

    }

    sales_column = find_column(

        dataframe,

        SALES_COLUMNS

    )

    if sales_column:

        kpis["total_sales"] = float(

            dataframe[sales_column].sum()

        )

        kpis["average_sales"] = float(

            dataframe[sales_column].mean()

        )

        kpis["highest_sales"] = float(

            dataframe[sales_column].max()

        )

        kpis["lowest_sales"] = float(

            dataframe[sales_column].min()

        )

    profit_column = find_column(

        dataframe,

        PROFIT_COLUMNS

    )

    if profit_column:

        kpis["total_profit"] = float(

            dataframe[profit_column].sum()

        )

        kpis["average_profit"] = float(

            dataframe[profit_column].mean()

        )

        kpis["highest_profit"] = float(

            dataframe[profit_column].max()

        )

        kpis["lowest_profit"] = float(

            dataframe[profit_column].min()

        )

    expense_column = find_column(

        dataframe,

        EXPENSE_COLUMNS

    )

    if expense_column:

        kpis["total_expenses"] = float(

            dataframe[expense_column].sum()

        )

        kpis["average_expenses"] = float(

            dataframe[expense_column].mean()

        )

    if sales_column and profit_column:

        total_sales = dataframe[sales_column].sum()

        total_profit = dataframe[profit_column].sum()

        if total_sales > 0:

            kpis["profit_margin"] = round(

                (total_profit / total_sales) * 100,

                2

            )

    return kpis