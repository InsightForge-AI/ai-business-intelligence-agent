"""
==========================================================
Enterprise Business Rules Engine
==========================================================

Author:
    AI Business Intelligence Agent

Purpose:
    Domain-aware business analysis engine that converts
    structured datasets into business metrics for LLMs.

Supported Domains
-----------------
• Retail
• Hospital
• Human Resources
• Finance
• Education
• Generic datasets

Output
------
Returns a structured business dictionary that can be
directly consumed by the LLM prompt.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

from analysis.kpi import (
    find_column,
    SALES_COLUMNS,
    PROFIT_COLUMNS,
)

# ==========================================================
# Constants
# ==========================================================

TOP_N = 10

DATASET_TYPES = (
    "retail",
    "hospital",
    "hr",
    "finance",
    "education",
    "generic",
)

# ==========================================================
# Safe Conversion Helpers
# ==========================================================


def safe_float(value: Any) -> Optional[float]:
    """
    Convert value to float.

    Returns None on failure.
    """

    try:
        return round(float(value), 2)
    except Exception:
        return None


def safe_int(value: Any) -> Optional[int]:
    """
    Convert value to int.

    Returns None on failure.
    """

    try:
        return int(value)
    except Exception:
        return None


def safe_string(value: Any) -> str:
    """
    Safe string conversion.
    """

    if pd.isna(value):
        return ""

    return str(value)


# ==========================================================
# Column Utilities
# ==========================================================


def actual_column(
    dataframe: pd.DataFrame,
    name: str
) -> Optional[str]:
    """
    Case-insensitive column lookup.

    Example

    bill

    Bill

    BILL

    all return the same column.
    """

    for column in dataframe.columns:

        if column.lower() == name.lower():

            return column

    return None


def column_exists(
    dataframe: pd.DataFrame,
    name: str
) -> bool:

    return actual_column(
        dataframe,
        name
    ) is not None


def numeric_columns(
    dataframe: pd.DataFrame
) -> List[str]:

    return list(

        dataframe

        .select_dtypes(
            include="number"
        )

        .columns

    )


def categorical_columns(
    dataframe: pd.DataFrame
) -> List[str]:

    return list(

        dataframe

        .select_dtypes(
            exclude="number"
        )

        .columns

    )


# ==========================================================
# Generic Statistics
# ==========================================================


def numeric_summary(
    dataframe: pd.DataFrame,
    column: str
) -> Dict[str, Any]:

    column = actual_column(
        dataframe,
        column
    )

    if column is None:

        return {}

    series = dataframe[column].dropna()

    if series.empty:

        return {}

    q1 = series.quantile(.25)
    q3 = series.quantile(.75)

    return {

        "count": int(series.count()),

        "missing": int(
            dataframe[column].isna().sum()
        ),

        "sum": safe_float(
            series.sum()
        ),

        "average": safe_float(
            series.mean()
        ),

        "median": safe_float(
            series.median()
        ),

        "minimum": safe_float(
            series.min()
        ),

        "maximum": safe_float(
            series.max()
        ),

        "range": safe_float(
            series.max() - series.min()
        ),

        "variance": safe_float(
            series.var()
        ),

        "std": safe_float(
            series.std()
        ),

        "q1": safe_float(q1),

        "q3": safe_float(q3),

        "iqr": safe_float(q3 - q1)

    }


# ==========================================================
# Distribution
# ==========================================================


def distribution(
    dataframe: pd.DataFrame,
    column: str,
    top: int = TOP_N
) -> Dict[str, int]:

    column = actual_column(
        dataframe,
        column
    )

    if column is None:

        return {}

    return (

        dataframe[column]

        .value_counts()

        .head(top)

        .to_dict()

    )


# ==========================================================
# Top Record
# ==========================================================


def top_record(
    dataframe: pd.DataFrame,
    value_column: str
) -> Dict[str, Any]:

    value_column = actual_column(
        dataframe,
        value_column
    )

    if value_column is None:

        return {}

    row = dataframe.loc[
        dataframe[value_column].idxmax()
    ]

    result = {}

    for column in dataframe.columns:

        value = row[column]

        if pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):

            result[column] = safe_float(
                value
            )

        else:

            result[column] = safe_string(
                value
            )

    return result


# ==========================================================
# Bottom Record
# ==========================================================


def bottom_record(
    dataframe: pd.DataFrame,
    value_column: str
) -> Dict[str, Any]:

    value_column = actual_column(
        dataframe,
        value_column
    )

    if value_column is None:

        return {}

    row = dataframe.loc[
        dataframe[value_column].idxmin()
    ]

    result = {}

    for column in dataframe.columns:

        value = row[column]

        if pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):

            result[column] = safe_float(
                value
            )

        else:

            result[column] = safe_string(
                value
            )

    return result


# ==========================================================
# Group Statistics
# ==========================================================


def group_statistics(
    dataframe: pd.DataFrame,
    group_column: str,
    value_column: str
) -> Dict[str, Any]:

    group_column = actual_column(
        dataframe,
        group_column
    )

    value_column = actual_column(
        dataframe,
        value_column
    )

    if (
        group_column is None or
        value_column is None
    ):
        return {}

    grouped = (

        dataframe

        .groupby(group_column)[value_column]

        .agg(

            count="count",

            total="sum",

            average="mean",

            minimum="min",

            maximum="max",

            median="median"

        )

        .round(2)

    )

    return grouped.to_dict(
        orient="index"
    )


# ==========================================================
# Overall Dataset Profile
# ==========================================================


def dataset_profile(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    return {

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "numeric_columns": len(
            numeric_columns(dataframe)
        ),

        "categorical_columns": len(
            categorical_columns(dataframe)
        ),

        "memory_mb": safe_float(
            dataframe.memory_usage(
                deep=True
            ).sum()
            / 1024
            / 1024
        )

    }

# ==========================================================
# Dataset Detection
# ==========================================================

RETAIL_KEYWORDS = {
    "product",
    "category",
    "sub-category",
    "sales",
    "profit",
    "region",
    "customer"
}

HOSPITAL_KEYWORDS = {
    "patientid",
    "patient",
    "department",
    "bill",
    "age",
    "daysadmitted",
    "doctor"
}

HR_KEYWORDS = {
    "employee",
    "employeeid",
    "salary",
    "designation",
    "department"
}

FINANCE_KEYWORDS = {
    "income",
    "expense",
    "balance",
    "revenue",
    "cost",
    "profit"
}

EDUCATION_KEYWORDS = {
    "student",
    "marks",
    "grade",
    "subject",
    "attendance"
}


def detect_dataset_type(
    dataframe: pd.DataFrame
) -> str:
    """
    Automatically detect dataset domain.

    Returns
    -------
    retail
    hospital
    hr
    finance
    education
    generic
    """

    columns = {
        column.lower().strip()
        for column in dataframe.columns
    }

    scores = {

        "retail": len(
            columns &
            RETAIL_KEYWORDS
        ),

        "hospital": len(
            columns &
            HOSPITAL_KEYWORDS
        ),

        "hr": len(
            columns &
            HR_KEYWORDS
        ),

        "finance": len(
            columns &
            FINANCE_KEYWORDS
        ),

        "education": len(
            columns &
            EDUCATION_KEYWORDS
        )

    }

    dataset = max(
        scores,
        key=scores.get
    )

    if scores[dataset] == 0:

        return "generic"

    return dataset


# ==========================================================
# Numeric Analysis
# ==========================================================

def analyze_numeric_columns(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    analysis = {}

    for column in numeric_columns(dataframe):

        analysis[column] = numeric_summary(
            dataframe,
            column
        )

    return analysis


# ==========================================================
# Categorical Analysis
# ==========================================================

def analyze_categorical_columns(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    analysis = {}

    for column in categorical_columns(dataframe):

        analysis[column] = {

            "unique_values": int(
                dataframe[column].nunique()
            ),

            "distribution": distribution(
                dataframe,
                column
            )

        }

    return analysis


# ==========================================================
# Missing Value Analysis
# ==========================================================

def missing_value_summary(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    result = {}

    rows = len(dataframe)

    for column in dataframe.columns:

        missing = int(
            dataframe[column]
            .isna()
            .sum()
        )

        result[column] = {

            "missing": missing,

            "percentage": safe_float(

                (missing / rows) * 100

            ) if rows else 0

        }

    return result


# ==========================================================
# Duplicate Analysis
# ==========================================================

def duplicate_summary(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    duplicates = int(
        dataframe
        .duplicated()
        .sum()
    )

    return {

        "duplicate_rows": duplicates,

        "duplicate_percentage": safe_float(

            duplicates /
            len(dataframe)
            * 100

        ) if len(dataframe) else 0

    }


# ==========================================================
# Correlation Analysis
# ==========================================================

def correlation_summary(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    numeric = dataframe.select_dtypes(
        include="number"
    )

    if numeric.shape[1] < 2:

        return {}

    correlation = numeric.corr()

    result = {}

    for row in correlation.index:

        values = {}

        for column in correlation.columns:

            if row == column:
                continue

            values[column] = safe_float(
                correlation.loc[
                    row,
                    column
                ]
            )

        result[row] = values

    return result


# ==========================================================
# Outlier Detection
# ==========================================================

def outlier_summary(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    summary = {}

    for column in numeric_columns(dataframe):

        series = dataframe[column]

        q1 = series.quantile(.25)

        q3 = series.quantile(.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = series[
            (series < lower) |
            (series > upper)
        ]

        summary[column] = {

            "count": int(
                len(outliers)
            ),

            "percentage": safe_float(

                len(outliers)
                /
                len(series)
                * 100

            ) if len(series) else 0

        }

    return summary


# ==========================================================
# Common Business Analysis
# ==========================================================

def common_analysis(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:
    """
    Analysis shared by every dataset.
    """

    return {

        "dataset_profile":
            dataset_profile(dataframe),

        "numeric_analysis":
            analyze_numeric_columns(dataframe),

        "categorical_analysis":
            analyze_categorical_columns(dataframe),

        "missing_values":
            missing_value_summary(dataframe),

        "duplicates":
            duplicate_summary(dataframe),

        "outliers":
            outlier_summary(dataframe),

        "correlations":
            correlation_summary(dataframe)

    }

# ==========================================================
# Retail Business Rules
# ==========================================================

def retail_rules(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:
    """
    Enterprise Retail Business Analysis.
    """

    business: Dict[str, Any] = {}

    # ------------------------------------------------------
    # Include Common Analysis
    # ------------------------------------------------------

    business.update(
        common_analysis(dataframe)
    )

    sales_column = find_column(
        dataframe,
        SALES_COLUMNS
    )

    profit_column = find_column(
        dataframe,
        PROFIT_COLUMNS
    )

    product_column = actual_column(
        dataframe,
        "Product"
    )

    category_column = actual_column(
        dataframe,
        "Category"
    )

    subcategory_column = actual_column(
        dataframe,
        "Sub-Category"
    )

    region_column = actual_column(
        dataframe,
        "Region"
    )

    customer_column = actual_column(
        dataframe,
        "Customer"
    )

    # ------------------------------------------------------
    # Overall Sales KPIs
    # ------------------------------------------------------

    if sales_column:

        business["sales_summary"] = numeric_summary(
            dataframe,
            sales_column
        )

        business["highest_sale"] = top_record(
            dataframe,
            sales_column
        )

        business["lowest_sale"] = bottom_record(
            dataframe,
            sales_column
        )

    # ------------------------------------------------------
    # Profit KPIs
    # ------------------------------------------------------

    if profit_column:

        business["profit_summary"] = numeric_summary(
            dataframe,
            profit_column
        )

        business["highest_profit"] = top_record(
            dataframe,
            profit_column
        )

        business["lowest_profit"] = bottom_record(
            dataframe,
            profit_column
        )

    # ------------------------------------------------------
    # Product Performance
    # ------------------------------------------------------

    if product_column and sales_column:

        grouped = (

            dataframe

            .groupby(product_column)

            .agg(

                total_sales=(sales_column, "sum"),

                average_sales=(sales_column, "mean"),

                max_sales=(sales_column, "max"),

                min_sales=(sales_column, "min"),

                transactions=(sales_column, "count")

            )

            .sort_values(
                "total_sales",
                ascending=False
            )

            .round(2)

        )

        business["product_performance"] = grouped.to_dict(
            orient="index"
        )

        business["top_products"] = (
            grouped.head(10)
            .to_dict(orient="index")
        )

        business["bottom_products"] = (
            grouped.tail(10)
            .to_dict(orient="index")
        )

    # ------------------------------------------------------
    # Category Performance
    # ------------------------------------------------------

    if category_column and sales_column:

        grouped = (

            dataframe

            .groupby(category_column)

            .agg(

                total_sales=(sales_column, "sum"),

                average_sales=(sales_column, "mean"),

                transactions=(sales_column, "count")

            )

            .sort_values(
                "total_sales",
                ascending=False
            )

            .round(2)

        )

        business["category_performance"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # SubCategory Performance
    # ------------------------------------------------------

    if subcategory_column and sales_column:

        grouped = (

            dataframe

            .groupby(subcategory_column)

            .agg(

                total_sales=(sales_column, "sum"),

                average_sales=(sales_column, "mean"),

                transactions=(sales_column, "count")

            )

            .sort_values(
                "total_sales",
                ascending=False
            )

            .round(2)

        )

        business["subcategory_performance"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # Regional Performance
    # ------------------------------------------------------

    if region_column and sales_column:

        grouped = (

            dataframe

            .groupby(region_column)

            .agg(

                total_sales=(sales_column, "sum"),

                average_sales=(sales_column, "mean"),

                transactions=(sales_column, "count")

            )

            .sort_values(
                "total_sales",
                ascending=False
            )

            .round(2)

        )

        business["regional_performance"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # Customer Performance
    # ------------------------------------------------------

    if customer_column and sales_column:

        grouped = (

            dataframe

            .groupby(customer_column)

            .agg(

                total_sales=(sales_column, "sum"),

                average_sales=(sales_column, "mean"),

                transactions=(sales_column, "count")

            )

            .sort_values(
                "total_sales",
                ascending=False
            )

            .round(2)

        )

        business["top_customers"] = (
            grouped.head(20)
            .to_dict(orient="index")
        )

    # ------------------------------------------------------
    # Profitability
    # ------------------------------------------------------

    if sales_column and profit_column:

        dataframe = dataframe.copy()

        dataframe["ProfitMargin"] = (

            dataframe[profit_column]

            /

            dataframe[sales_column]

        ) * 100

        business["profit_margin"] = {

            "average_margin": safe_float(
                dataframe["ProfitMargin"].mean()
            ),

            "highest_margin": safe_float(
                dataframe["ProfitMargin"].max()
            ),

            "lowest_margin": safe_float(
                dataframe["ProfitMargin"].min()
            )

        }

    # ------------------------------------------------------
    # Business Highlights
    # ------------------------------------------------------

    highlights = {}

    if sales_column:

        highlights["total_sales"] = safe_float(
            dataframe[sales_column].sum()
        )

        highlights["average_sale"] = safe_float(
            dataframe[sales_column].mean()
        )

    if profit_column:

        highlights["total_profit"] = safe_float(
            dataframe[profit_column].sum()
        )

        highlights["average_profit"] = safe_float(
            dataframe[profit_column].mean()
        )

    if product_column:

        highlights["unique_products"] = int(
            dataframe[product_column].nunique()
        )

    if customer_column:

        highlights["unique_customers"] = int(
            dataframe[customer_column].nunique()
        )

    if region_column:

        highlights["regions"] = int(
            dataframe[region_column].nunique()
        )

    business["business_highlights"] = highlights

    return business

# ==========================================================
# Hospital Business Rules
# ==========================================================

def hospital_rules(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:
    """
    Enterprise Hospital Business Analysis.
    """

    business: Dict[str, Any] = {}

    # ------------------------------------------------------
    # Common Analysis
    # ------------------------------------------------------

    business.update(
        common_analysis(dataframe)
    )

    patient_column = actual_column(dataframe, "PatientID")
    department_column = actual_column(dataframe, "Department")
    bill_column = actual_column(dataframe, "Bill")
    stay_column = actual_column(dataframe, "DaysAdmitted")
    age_column = actual_column(dataframe, "Age")
    doctor_column = actual_column(dataframe, "Doctor")

    # ------------------------------------------------------
    # Hospital Summary
    # ------------------------------------------------------

    summary = {}

    summary["total_patients"] = len(dataframe)

    if department_column:
        summary["departments"] = dataframe[
            department_column
        ].nunique()

    if doctor_column:
        summary["doctors"] = dataframe[
            doctor_column
        ].nunique()

    if bill_column:
        summary["total_bill"] = safe_float(
            dataframe[bill_column].sum()
        )

        summary["average_bill"] = safe_float(
            dataframe[bill_column].mean()
        )

    if stay_column:
        summary["average_stay"] = safe_float(
            dataframe[stay_column].mean()
        )

    if age_column:
        summary["average_age"] = safe_float(
            dataframe[age_column].mean()
        )

    business["hospital_summary"] = summary

    # ------------------------------------------------------
    # Bill Statistics
    # ------------------------------------------------------

    if bill_column:

        business["bill_statistics"] = numeric_summary(
            dataframe,
            bill_column
        )

        business["highest_bill"] = top_record(
            dataframe,
            bill_column
        )

        business["lowest_bill"] = bottom_record(
            dataframe,
            bill_column
        )

    # ------------------------------------------------------
    # Stay Statistics
    # ------------------------------------------------------

    if stay_column:

        business["stay_statistics"] = numeric_summary(
            dataframe,
            stay_column
        )

        business["longest_admission"] = top_record(
            dataframe,
            stay_column
        )

        business["shortest_admission"] = bottom_record(
            dataframe,
            stay_column
        )

    # ------------------------------------------------------
    # Age Statistics
    # ------------------------------------------------------

    if age_column:

        business["age_statistics"] = numeric_summary(
            dataframe,
            age_column
        )

    # ------------------------------------------------------
    # Department Billing
    # ------------------------------------------------------

    if department_column and bill_column:

        grouped = (

            dataframe

            .groupby(department_column)

            .agg(

                patients=(patient_column, "count"),

                total_bill=(bill_column, "sum"),

                average_bill=(bill_column, "mean"),

                maximum_bill=(bill_column, "max"),

                minimum_bill=(bill_column, "min")

            )

            .sort_values(
                "total_bill",
                ascending=False
            )

            .round(2)

        )

        business["department_billing"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # Department Admissions
    # ------------------------------------------------------

    if department_column and stay_column:

        grouped = (

            dataframe

            .groupby(department_column)

            .agg(

                patients=(patient_column, "count"),

                average_stay=(stay_column, "mean"),

                maximum_stay=(stay_column, "max"),

                minimum_stay=(stay_column, "min")

            )

            .sort_values(
                "average_stay",
                ascending=False
            )

            .round(2)

        )

        business["department_admissions"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # Department Age Profile
    # ------------------------------------------------------

    if department_column and age_column:

        grouped = (

            dataframe

            .groupby(department_column)

            .agg(

                average_age=(age_column, "mean"),

                youngest=(age_column, "min"),

                oldest=(age_column, "max")

            )

            .round(2)

        )

        business["department_age_profile"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # Patient Distribution
    # ------------------------------------------------------

    if department_column:

        business["patients_by_department"] = distribution(
            dataframe,
            department_column
        )

    # ------------------------------------------------------
    # Top Departments
    # ------------------------------------------------------

    if department_column and bill_column:

        top_departments = (

            dataframe

            .groupby(department_column)[bill_column]

            .sum()

            .sort_values(
                ascending=False
            )

            .head(10)

        )

        business["top_departments"] = {

            department: safe_float(value)

            for department, value

            in top_departments.items()

        }

    # ------------------------------------------------------
    # Business Highlights
    # ------------------------------------------------------

    highlights = {}

    if bill_column:

        highlights["highest_bill"] = safe_float(
            dataframe[bill_column].max()
        )

        highlights["lowest_bill"] = safe_float(
            dataframe[bill_column].min()
        )

    if stay_column:

        highlights["longest_stay"] = safe_float(
            dataframe[stay_column].max()
        )

        highlights["shortest_stay"] = safe_float(
            dataframe[stay_column].min()
        )

    if age_column:

        highlights["oldest_patient"] = safe_float(
            dataframe[age_column].max()
        )

        highlights["youngest_patient"] = safe_float(
            dataframe[age_column].min()
        )

    business["business_highlights"] = highlights

    return business

# ==========================================================
# HR Business Rules
# ==========================================================

def hr_rules(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    business = {}

    business.update(
        common_analysis(dataframe)
    )

    employee_column = actual_column(
        dataframe,
        "Employee"
    ) or actual_column(
        dataframe,
        "EmployeeID"
    )

    department_column = actual_column(
        dataframe,
        "Department"
    )

    salary_column = actual_column(
        dataframe,
        "Salary"
    )

    designation_column = actual_column(
        dataframe,
        "Designation"
    )

    # ------------------------------------------------------
    # Salary Statistics
    # ------------------------------------------------------

    if salary_column:

        business["salary_statistics"] = numeric_summary(
            dataframe,
            salary_column
        )

        business["highest_salary"] = top_record(
            dataframe,
            salary_column
        )

        business["lowest_salary"] = bottom_record(
            dataframe,
            salary_column
        )

    # ------------------------------------------------------
    # Department Salary
    # ------------------------------------------------------

    if department_column and salary_column:

        business["department_salary"] = group_statistics(
            dataframe,
            department_column,
            salary_column
        )

    # ------------------------------------------------------
    # Employee Distribution
    # ------------------------------------------------------

    if department_column:

        business["employees_by_department"] = distribution(
            dataframe,
            department_column
        )

    if designation_column:

        business["designation_distribution"] = distribution(
            dataframe,
            designation_column
        )

    # ------------------------------------------------------
    # Business Highlights
    # ------------------------------------------------------

    highlights = {}

    if employee_column:

        highlights["employees"] = int(
            dataframe[employee_column].nunique()
        )

    if department_column:

        highlights["departments"] = int(
            dataframe[department_column].nunique()
        )

    if salary_column:

        highlights["average_salary"] = safe_float(
            dataframe[salary_column].mean()
        )

        highlights["total_salary"] = safe_float(
            dataframe[salary_column].sum()
        )

    business["business_highlights"] = highlights

    return business


# ==========================================================
# Finance Business Rules
# ==========================================================

def finance_rules(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    business = {}

    business.update(
        common_analysis(dataframe)
    )

    numeric = numeric_columns(
        dataframe
    )

    for column in numeric:

        business[column] = numeric_summary(
            dataframe,
            column
        )

        business[f"{column}_highest"] = top_record(
            dataframe,
            column
        )

        business[f"{column}_lowest"] = bottom_record(
            dataframe,
            column
        )

    income_column = actual_column(
        dataframe,
        "Income"
    )

    expense_column = actual_column(
        dataframe,
        "Expense"
    )

    if income_column and expense_column:

        dataframe = dataframe.copy()

        dataframe["NetProfit"] = (

            dataframe[income_column]

            -

            dataframe[expense_column]

        )

        business["net_profit"] = {

            "total": safe_float(
                dataframe["NetProfit"].sum()
            ),

            "average": safe_float(
                dataframe["NetProfit"].mean()
            ),

            "maximum": safe_float(
                dataframe["NetProfit"].max()
            ),

            "minimum": safe_float(
                dataframe["NetProfit"].min()
            )

        }

    return business


# ==========================================================
# Education Business Rules
# ==========================================================

def education_rules(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:

    business = {}

    business.update(
        common_analysis(dataframe)
    )

    student_column = actual_column(
        dataframe,
        "Student"
    )

    marks_column = actual_column(
        dataframe,
        "Marks"
    )

    grade_column = actual_column(
        dataframe,
        "Grade"
    )

    subject_column = actual_column(
        dataframe,
        "Subject"
    )

    # ------------------------------------------------------
    # Marks
    # ------------------------------------------------------

    if marks_column:

        business["marks_statistics"] = numeric_summary(
            dataframe,
            marks_column
        )

        business["highest_marks"] = top_record(
            dataframe,
            marks_column
        )

        business["lowest_marks"] = bottom_record(
            dataframe,
            marks_column
        )

    # ------------------------------------------------------
    # Grade Distribution
    # ------------------------------------------------------

    if grade_column:

        business["grade_distribution"] = distribution(
            dataframe,
            grade_column
        )

    # ------------------------------------------------------
    # Subject Performance
    # ------------------------------------------------------

    if subject_column and marks_column:

        grouped = (

            dataframe

            .groupby(subject_column)

            .agg(

                students=(marks_column, "count"),

                average_marks=(marks_column, "mean"),

                maximum_marks=(marks_column, "max"),

                minimum_marks=(marks_column, "min")

            )

            .round(2)

        )

        business["subject_performance"] = grouped.to_dict(
            orient="index"
        )

    # ------------------------------------------------------
    # Business Highlights
    # ------------------------------------------------------

    highlights = {}

    if student_column:

        highlights["students"] = int(
            dataframe[student_column].nunique()
        )

    if subject_column:

        highlights["subjects"] = int(
            dataframe[subject_column].nunique()
        )

    if marks_column:

        highlights["average_marks"] = safe_float(
            dataframe[marks_column].mean()
        )

    business["business_highlights"] = highlights

    return business

# ==========================================================
# Generic Business Rules
# ==========================================================

def generic_rules(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:
    """
    Generic analysis for unknown datasets.
    """

    business = {}

    # Shared analysis
    business.update(
        common_analysis(dataframe)
    )

    # ------------------------------------------------------
    # Numeric Columns
    # ------------------------------------------------------

    numeric = numeric_columns(
        dataframe
    )

    for column in numeric:

        business[column] = numeric_summary(
            dataframe,
            column
        )

        business[f"{column}_highest"] = top_record(
            dataframe,
            column
        )

        business[f"{column}_lowest"] = bottom_record(
            dataframe,
            column
        )

    # ------------------------------------------------------
    # Categorical Columns
    # ------------------------------------------------------

    for column in categorical_columns(dataframe):

        business[f"{column}_distribution"] = distribution(
            dataframe,
            column
        )

    # ------------------------------------------------------
    # Dataset Highlights
    # ------------------------------------------------------

    business["business_highlights"] = {

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "numeric_columns": len(
            numeric_columns(dataframe)
        ),

        "categorical_columns": len(
            categorical_columns(dataframe)
        )

    }

    return business


# ==========================================================
# Rule Registry
# ==========================================================

RULES = {

    "retail": retail_rules,

    "hospital": hospital_rules,

    "hr": hr_rules,

    "finance": finance_rules,

    "education": education_rules,

    "generic": generic_rules

}


# ==========================================================
# Main Entry
# ==========================================================

def analyze_business(
    dataframe: pd.DataFrame
) -> Dict[str, Any]:
    """
    Enterprise Business Analysis Entry Point.

    Parameters
    ----------
    dataframe

        Input dataframe.

    Returns
    -------
    Dictionary containing structured
    business context.
    """

    if dataframe.empty:

        return {

            "status": "failed",

            "reason": "Dataset is empty."

        }

    try:

        dataset = detect_dataset_type(
            dataframe
        )

        analyzer = RULES.get(
            dataset,
            generic_rules
        )

        result = analyzer(
            dataframe
        )

        result["dataset_type"] = dataset

        result["analysis_status"] = "completed"

        return result

    except Exception as error:

        return {

            "analysis_status": "failed",

            "dataset_type": "unknown",

            "error": str(error)

        }