"""
QA test suite for ML Team A.
Covers preprocess/analyze/insights unit logic plus the POST /ml/analyze
contract -- including proof that the user's natural-language query text
is completely ignored by the "string" request path.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from ml.teamA.src.preprocess import preprocess  # noqa: E402
from ml.teamA.src.analysis import analyze  # noqa: E402
from ml.teamA.src.insights import get_insights  # noqa: E402


# ---------------------------------------------------------------------------
# preprocess()
# ---------------------------------------------------------------------------

class TestPreprocess:

    def test_missing_file_returns_empty_dataframe_not_error(self, tmp_path):
        df = preprocess(str(tmp_path / "does_not_exist.csv"))
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_missing_columns_are_backfilled(self, tmp_path):
        csv = tmp_path / "sales.csv"
        csv.write_text("other_col\n1\n2\n")
        df = preprocess(str(csv))
        assert "product" in df.columns
        assert "total_sales" in df.columns
        assert (df["product"] == "unknown").all()

    def test_real_repo_data_file_loads(self):
        real_path = REPO_ROOT / "ml" / "teamA" / "data" / "sales_data.csv"
        df = preprocess(str(real_path))
        assert not df.empty
        assert "product" in df.columns
        assert "total_sales" in df.columns


# ---------------------------------------------------------------------------
# analyze()
# ---------------------------------------------------------------------------

class TestAnalyze:

    def test_empty_dataframe(self):
        res = analyze(pd.DataFrame())
        assert res["trend"] == "no data"
        assert res["top_product"] is None

    def test_all_zero_sales_no_trend(self):
        df = pd.DataFrame({"product": ["a", "b"], "total_sales": [0, 0]})
        res = analyze(df)
        assert res["trend"] == "no trend"
        assert res["top_product"] is None

    def test_all_nan_sales_marked_invalid(self):
        df = pd.DataFrame({"product": ["a", "b"], "total_sales": ["x", "y"]})
        res = analyze(df)
        assert res["trend"] == "invalid"
        assert res["top_product"] == "null"

    def test_increasing_trend(self):
        df = pd.DataFrame(
            {"product": ["a", "b", "c"], "total_sales": [10, 20, 30]}
        )
        res = analyze(df)
        assert res["trend"] == "increasing"
        assert res["top_product"] == "c"
        assert res["total_sales"] == 60

    def test_decreasing_trend(self):
        df = pd.DataFrame(
            {"product": ["a", "b", "c"], "total_sales": [30, 20, 10]}
        )
        res = analyze(df)
        assert res["trend"] == "decreasing"

    def test_single_row_is_stable(self):
        df = pd.DataFrame({"product": ["a"], "total_sales": [42]})
        res = analyze(df)
        assert res["trend"] == "stable"
        assert res["top_product"] == "a"

    def test_negative_sales_values_are_accepted_without_validation(self):
        # Nothing in the pipeline rejects negative sales figures, which is
        # nonsensical for a "total_sales" business metric. Documents a
        # missing input-validation boundary, not a crash.
        df = pd.DataFrame({"product": ["a", "b"], "total_sales": [-100, -50]})
        res = analyze(df)
        assert res["total_sales"] == -150
        assert res["error"] is None

    def test_partial_nan_trend_labeled_partial(self):
        df = pd.DataFrame(
            {"product": ["a", "b", "c"], "total_sales": [10, "bad", 30]}
        )
        res = analyze(df)
        assert res["trend"] == "partial"

    def test_duplicate_max_sales_products_does_not_crash(self):
        # Two products tie for the max value. `.loc[idxmax(), "product"]`
        # returns a single row from a *duplicated total_sales* value, which
        # is safe -- but if the *index* itself is duplicated (e.g. a
        # dataframe built upstream without reset_index), `.loc` can instead
        # return a Series and blow up the f-string in insights.py. Regression
        # guard for that shape.
        df = pd.DataFrame(
            {"product": ["a", "b"], "total_sales": [50, 50]},
            index=[0, 0],
        )
        res = analyze(df)
        assert res["error"] is None, (
            "Duplicate index caused .loc[idxmax(), 'product'] to return a "
            f"Series instead of a scalar: {res}"
        )


# ---------------------------------------------------------------------------
# get_insights()
# ---------------------------------------------------------------------------

class TestInsights:

    def test_halts_on_invalid(self):
        out = get_insights({"trend": "invalid"})
        assert "halted" in out["insights"].lower()

    def test_normal_message(self):
        out = get_insights(
            {"total_sales": 100, "top_product": "Widget", "trend": "increasing"}
        )
        assert "Widget" in out["insights"]
        assert "100" in out["insights"]

    def test_none_top_product_renders_as_none_text(self):
        out = get_insights(
            {"total_sales": 0, "top_product": None, "trend": "no trend"}
        )
        assert "None is the top performing product" in out["insights"]


# ---------------------------------------------------------------------------
# HTTP contract tests: POST /ml/analyze
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from ml.teamA.api.main import app
    return TestClient(app)


class TestMlApiContract:

    def test_string_query_ignores_its_own_content(self, client):
        """
        CRITICAL business-logic finding: backend/app/services/ml_service.py
        always sends the user's raw chat text as `{"data": query}`. Because
        req.data is a str, /ml/analyze *always* reloads the same static
        ml/teamA/data/sales_data.csv, discarding the query entirely. Two
        completely different natural-language questions must produce byte-
        identical responses -- proving the ML "assistant" never actually
        reads what the user asked.
        """
        r1 = client.post("/ml/analyze", json={"data": "what were the sales in january"})
        r2 = client.post("/ml/analyze", json={"data": "show me a completely unrelated question about penguins"})
        assert r1.status_code == 200 and r2.status_code == 200
        assert r1.json() == r2.json(), (
            "ML output must not be identical for unrelated queries -- but it is, "
            "because the string branch ignores req.data entirely."
        )

    def test_empty_string_query_still_returns_full_csv_analysis(self, client):
        r = client.post("/ml/analyze", json={"data": ""})
        assert r.status_code == 200
        assert "insights" in r.json()

    def test_dict_query_uses_provided_numbers(self, client):
        r = client.post(
            "/ml/analyze",
            json={"data": {"widget": 10.0, "gadget": 90.0}},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["top_product"] == "gadget"
        assert body["total_sales"] == 100

    def test_dict_query_with_non_numeric_value_returns_422(self, client):
        r = client.post(
            "/ml/analyze",
            json={"data": {"widget": "not-a-number"}},
        )
        assert r.status_code == 422

    def test_missing_data_field_returns_422(self, client):
        r = client.post("/ml/analyze", json={})
        assert r.status_code == 422

    def test_negative_dict_values_accepted_without_validation(self, client):
        r = client.post("/ml/analyze", json={"data": {"widget": -5.0}})
        assert r.status_code == 200
        assert r.json()["total_sales"] == -5

    def test_payload_over_the_size_cap_is_rejected(self, client):
        # MaxBodySizeMiddleware in ml/teamA/api/main.py caps requests at
        # 2MB; this used to have no limit at all.
        r = client.post("/ml/analyze", json={"data": "x" * (3 * 1024 * 1024)})
        assert r.status_code == 413
