import pandas as pd
import numpy as np


def analyze(df, col_map):
    res = {"total_sales": 0, "top_product": None, "trend": "stable", "rankings": [], "error": None}
    try:
        num_col = col_map.get("numeric")
        cat_col = col_map.get("category")
        dat_col = col_map.get("date")

        if df.empty or not num_col:
            res["trend"] = "no data"
            return res

        sales_series = pd.to_numeric(df[num_col], errors="coerce")
        has_nans = sales_series.isna().any()
        clean = sales_series.fillna(0)
        total = clean.sum()

        res["total_sales"] = float(total) if total % 1 else int(total)
        res["total_sales_formatted"] = f"₹{int(total):,}"

        if total == 0 and not has_nans:
            res["top_product"] = None
            res["trend"] = "no trend"
            return res

        if total == 0 and has_nans:
            res["top_product"] = None
            res["trend"] = "invalid"
            return res

        if cat_col and cat_col in df.columns:
            cat_totals = (
                df.groupby(cat_col)[num_col]
                .apply(lambda x: pd.to_numeric(x, errors="coerce").fillna(0).sum())
                .sort_values(ascending=False)
            )
            res["top_product"] = str(cat_totals.index[0])
            res["rankings"] = [
                {"product": str(k), "total": int(v), "share": round(float(v) / total * 100, 1)}
                for k, v in cat_totals.items()
            ]
        else:
            res["top_product"] = "unknown"

        if has_nans:
            res["trend"] = "partial"
            return res

        # Case 11 — Single row
        if len(clean) == 1:
            res["trend"] = "stable"
            return res

        # Trend via linear regression
        ts = clean
        if dat_col and dat_col in df.columns:
            df_s = df.copy()
            df_s[dat_col] = pd.to_datetime(df_s[dat_col], dayfirst=True, errors="coerce")
            df_s = df_s.dropna(subset=[dat_col]).sort_values(dat_col)
            ts = pd.to_numeric(df_s[num_col], errors="coerce").fillna(0)

        if len(ts) >= 2:
            slope = float(np.polyfit(np.arange(len(ts)), ts.values, 1)[0])
            rel   = abs(slope) / (ts.mean() + 1e-9)
            if slope > 0 and rel > 0.01:
                res["trend"] = "increasing"
            elif slope < 0 and rel > 0.01:
                res["trend"] = "decreasing"

    except Exception as e:
        res["trend"] = "invalid"
        res["error"] = str(e)

    return res