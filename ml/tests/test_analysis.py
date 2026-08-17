"""
Tests for the ML service's deterministic analysis pipeline (loader,
profiler, KPI calculator, outlier detection, trend analysis). These test
files were previously empty stubs (docstring only, zero real tests) --
this is the first real coverage for this module.

DeepSeek/LLM-backed pieces (analysis.py's run_analysis, llm/*) are not
covered here since no LLM runtime is available in this environment; see
test_llm.py for a mocked-boundary approach to that layer instead.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # ml/

from analysis.loader import load_data
from analysis.profiler import generate_profile
from analysis.kpi import calculate_kpis, find_column
from analysis.outlier import detect_outliers, remove_outliers
from analysis.trend import detect_dataset_type, analyze_trends


class TestLoadData:

    def test_list_of_records(self):
        df = load_data([{"a": 1}, {"a": 2}])
        assert len(df) == 2

    def test_single_dict_becomes_one_row(self):
        df = load_data({"a": 1, "b": 2})
        assert len(df) == 1
        assert list(df.columns) == ["a", "b"]

    def test_dataframe_passthrough(self):
        original = pd.DataFrame({"a": [1, 2]})
        assert load_data(original) is original

    def test_none_raises_value_error(self):
        with pytest.raises(ValueError):
            load_data(None)

    def test_empty_list_raises_value_error(self):
        with pytest.raises(ValueError):
            load_data([])

    def test_unsupported_type_raises_type_error(self):
        with pytest.raises(TypeError):
            load_data("just a string")


class TestGenerateProfile:

    def test_basic_profile_shape(self):
        df = pd.DataFrame({"product": ["a", "b"], "sales": [10, 20]})
        profile = generate_profile(df)
        assert profile["rows"] == 2
        assert profile["columns"] == 2
        assert "sales" in profile["numeric_columns"]
        assert "product" in profile["categorical_columns"]

    def test_missing_values_counted(self):
        df = pd.DataFrame({"a": [1, None, 3]})
        profile = generate_profile(df)
        assert profile["missing_values"]["a"] == 1


class TestCalculateKpis:

    def test_finds_sales_column_case_insensitively(self):
        df = pd.DataFrame({"REVENUE": [100, 200, 300]})
        assert find_column(df, ["Sales", "Revenue"]) == "REVENUE"

    def test_no_matching_column_returns_none(self):
        df = pd.DataFrame({"unrelated": [1, 2]})
        assert find_column(df, ["Sales", "Revenue"]) is None

    def test_sales_kpis_computed(self):
        df = pd.DataFrame({"Sales": [100, 200, 300]})
        kpis = calculate_kpis(df)
        assert kpis["total_sales"] == 600
        assert kpis["average_sales"] == 200
        assert kpis["highest_sales"] == 300
        assert kpis["lowest_sales"] == 100

    def test_profit_margin_computed_when_both_present(self):
        df = pd.DataFrame({"Sales": [1000], "Profit": [250]})
        kpis = calculate_kpis(df)
        assert kpis["profit_margin"] == 25.0

    def test_no_profit_margin_when_sales_missing(self):
        df = pd.DataFrame({"Profit": [250]})
        kpis = calculate_kpis(df)
        assert "profit_margin" not in kpis

    def test_zero_sales_does_not_divide_by_zero(self):
        df = pd.DataFrame({"Sales": [0, 0], "Profit": [0, 0]})
        kpis = calculate_kpis(df)
        assert "profit_margin" not in kpis  # guarded by `if total_sales > 0`


class TestOutlierDetection:

    def test_detects_obvious_outlier(self):
        df = pd.DataFrame({"value": [10, 11, 12, 13, 11, 12, 1000]})
        report = detect_outliers(df)
        assert report["total_outliers"] >= 1
        assert report["columns"]["value"] >= 1

    def test_no_outliers_in_uniform_data(self):
        df = pd.DataFrame({"value": [10, 10, 10, 10]})
        report = detect_outliers(df)
        assert report["total_outliers"] == 0

    def test_remove_outliers_shrinks_dataframe(self):
        df = pd.DataFrame({"value": [10, 11, 12, 13, 11, 12, 1000]})
        cleaned, report = remove_outliers(df)
        assert len(cleaned) < len(df)
        assert report["value"] >= 1

    def test_non_numeric_columns_ignored(self):
        df = pd.DataFrame({"label": ["a", "b", "c"]})
        report = detect_outliers(df)
        assert report["total_outliers"] == 0
        assert report["columns"] == {}


class TestTrendAnalysis:

    def test_detects_retail_dataset(self):
        df = pd.DataFrame({"Product": ["a"], "Sales": [1]})
        assert detect_dataset_type(df) == "retail"

    def test_detects_hospital_dataset(self):
        df = pd.DataFrame({"Department": ["ER"], "Bill": [100]})
        assert detect_dataset_type(df) == "hospital"

    def test_detects_hr_dataset(self):
        df = pd.DataFrame({"Employee": ["x"], "Salary": [1]})
        assert detect_dataset_type(df) == "hr"

    def test_unknown_dataset_falls_back_to_generic(self):
        df = pd.DataFrame({"foo": [1], "bar": [2]})
        assert detect_dataset_type(df) == "generic"

    def test_retail_trend_groups_sales_by_time(self):
        df = pd.DataFrame({
            "Product": ["a", "b"],
            "Date": ["2024-01", "2024-02"],
            "Sales": [100, 200],
        })
        trends = analyze_trends(df)
        assert trends["sales_trend"]["2024-01"] == 100.0
        assert trends["sales_trend"]["2024-02"] == 200.0

    def test_generic_trend_summarizes_numeric_columns(self):
        df = pd.DataFrame({"x": [1, 2, 3]})
        trends = analyze_trends(df)
        assert trends["x"]["average"] == 2.0
        assert trends["x"]["minimum"] == 1.0
        assert trends["x"]["maximum"] == 3.0
