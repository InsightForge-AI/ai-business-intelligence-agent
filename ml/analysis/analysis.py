"""
==========================================================
Business Analysis
==========================================================

Responsibilities
----------------
• Execute complete business analysis
• Calculate KPIs
• Generate statistics
• Execute business rules
• Detect trends and outliers
• Build business context
• Call DeepSeek LLM
• Return complete analysis
"""

from __future__ import annotations

import pandas as pd

from analysis.kpi import calculate_kpis
from analysis.statistics import calculate_statistics
from analysis.business_rules import analyze_business
from analysis.trend import analyze_trends
from analysis.outlier import detect_outliers

from llm.llm_service import generate_insights


def build_business_kpis(
    dataframe: pd.DataFrame,
    business: dict,
    base_kpis: dict
) -> dict:
    """
    Build dataset-specific business KPIs.
    """

    kpis = dict(base_kpis)

    dataset = business.get(
        "dataset_type",
        "generic"
    )

    # --------------------------------------------------
    # Hospital
    # --------------------------------------------------

    if dataset == "hospital":

        summary = business.get(
            "hospital_summary",
            {}
        )

        highlights = business.get(
            "business_highlights",
            {}
        )

        kpis.update({

            "total_records": summary.get(
                "total_patients",
                len(dataframe)
            ),

            "departments": summary.get(
                "departments"
            ),

            "doctors": summary.get(
                "doctors"
            ),

            "average_age": summary.get(
                "average_age"
            ),

            "average_stay": summary.get(
                "average_stay"
            ),

            "total_bill": summary.get(
                "total_bill"
            ),

            "average_bill": summary.get(
                "average_bill"
            ),

            "highest_bill": highlights.get(
                "highest_bill"
            ),

            "lowest_bill": highlights.get(
                "lowest_bill"
            )

        })

    # --------------------------------------------------
    # Retail
    # --------------------------------------------------

    elif dataset == "retail":

        highlights = business.get(
            "business_highlights",
            {}
        )

        kpis.update(highlights)

    # --------------------------------------------------
    # HR
    # --------------------------------------------------

    elif dataset == "hr":

        highlights = business.get(
            "business_highlights",
            {}
        )

        kpis.update(highlights)

    # --------------------------------------------------
    # Finance
    # --------------------------------------------------

    elif dataset == "finance":

        net_profit = business.get(
            "net_profit",
            {}
        )

        kpis.update(net_profit)

    # --------------------------------------------------
    # Education
    # --------------------------------------------------

    elif dataset == "education":

        highlights = business.get(
            "business_highlights",
            {}
        )

        kpis.update(highlights)

    return kpis


async def run_analysis(
    dataframe: pd.DataFrame,
    query: str,
    metadata: dict,
    profile: dict
) -> dict:
    """
    Execute the complete ML business analysis pipeline.
    """

    # --------------------------------------------------
    # KPI Analysis
    # --------------------------------------------------

    base_kpis = calculate_kpis(
        dataframe
    )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    statistics = calculate_statistics(
        dataframe
    )

    # --------------------------------------------------
    # Business Rules
    # --------------------------------------------------

    business = analyze_business(
        dataframe
    )

    # --------------------------------------------------
    # Build Business KPIs
    # --------------------------------------------------

    kpis = build_business_kpis(
        dataframe,
        business,
        base_kpis
    )

    # --------------------------------------------------
    # Trend Analysis
    # --------------------------------------------------

    trends = analyze_trends(
        dataframe
    )

    # --------------------------------------------------
    # Outlier Detection
    # --------------------------------------------------

    outliers = detect_outliers(
        dataframe
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    analysis_metadata = {

        **metadata,

        "dataset_type": business.get(
            "dataset_type",
            "generic"
        ),

        "rows": len(dataframe),

        "columns": len(
            dataframe.columns
        )

    }

    # --------------------------------------------------
    # Business Context
    # --------------------------------------------------

    business_context = {

        "query": query,

        "metadata": analysis_metadata,

        "profile": profile,

        "kpis": kpis,

        "statistics": statistics,

        "business": business,

        "trends": trends,

        "outliers": outliers

    }

    # --------------------------------------------------
    # Generate AI Insights
    # --------------------------------------------------

    llm_response = await generate_insights(
        business_context
    )

    # --------------------------------------------------
    # Final Result
    # --------------------------------------------------

    return {

        "kpis": kpis,

        "profile": profile,

        "statistics": statistics,

        "business": business,

        "trends": trends,

        "outliers": outliers,

        "metadata": analysis_metadata,

        "llm": llm_response

    }