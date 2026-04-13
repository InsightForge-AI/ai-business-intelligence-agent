from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_sales_data(file_path: str | Path) -> pd.DataFrame:
    sales_df = pd.read_csv(file_path)
    sales_df.columns = (
        sales_df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )

    for column in ["product", "category", "status"]:
        if column in sales_df.columns:
            sales_df[column] = sales_df[column].astype(str).str.strip().str.title()
            sales_df[column] = sales_df[column].replace({"": pd.NA, "Nan": pd.NA, "None": pd.NA})

    for column in ["quantity", "price", "total"]:
        if column in sales_df.columns:
            sales_df[column] = _to_numeric(sales_df[column])

    if "order_date" in sales_df.columns:
        sales_df["order_date"] = pd.to_datetime(sales_df["order_date"], errors="coerce")

    if {"quantity", "price", "total"}.issubset(sales_df.columns):
        calculated_total = sales_df["quantity"] * sales_df["price"]
        sales_df["total"] = sales_df["total"].fillna(calculated_total)

    required_columns = ["product", "order_date", "total"]
    sales_df = sales_df.dropna(subset=[column for column in required_columns if column in sales_df.columns])

    if "total" in sales_df.columns:
        sales_df = sales_df[sales_df["total"] > 0]

    return sales_df.reset_index(drop=True)


def _to_numeric(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    cleaned = cleaned.replace({"": pd.NA, "-": pd.NA, ".": pd.NA})
    return pd.to_numeric(cleaned, errors="coerce")
