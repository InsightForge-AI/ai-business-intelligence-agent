from __future__ import annotations

import pandas as pd


def get_insights(sales_df: pd.DataFrame) -> dict[str, object]:
    ordered = sales_df.sort_values("order_date").reset_index(drop=True)
    total_sales = round(float(ordered["total"].sum()), 2)

    revenue_by_product = ordered.groupby("product")["total"].sum().sort_values(ascending=False)
    top_product = str(revenue_by_product.index[0])

    if len(ordered) < 2:
        trend = "stable"
    else:
        trend = (
            "increasing"
            if float(ordered["total"].iloc[-1]) > float(ordered["total"].iloc[0])
            else "decreasing"
        )

    insights = (
        f"Processed {len(ordered)} valid sales rows. "
        f"{top_product} is the top product, total sales are {total_sales}, "
        f"and the sales trend is {trend}."
    )

    return {
        "total_sales": total_sales,
        "top_product": top_product,
        "trend": trend,
        "insights": insights,
    }
