"""
==========================================================
DeepSeek Prompt Templates
==========================================================

Author:
    AI Business Intelligence Agent

Purpose
-------
Centralized prompt engineering module responsible for:

• Building optimized prompts for DeepSeek
• Reducing hallucinations
• Enforcing JSON output
• Providing domain-specific instructions
• Improving response consistency

This module MUST NOT perform business analysis.

It ONLY converts structured business context into
LLM-ready prompts.
"""

from __future__ import annotations

import json

from typing import Any, Dict


# ==========================================================
# Prompt Configuration
# ==========================================================

MODEL_NAME = "deepseek-r1:1.5b"

MAX_SUMMARY_WORDS = 80

DEFAULT_INSIGHTS = 5

DEFAULT_RECOMMENDATIONS = 5

SUPPORTED_DATASETS = (
    "retail",
    "hospital",
    "finance",
    "hr",
    "education",
    "generic"
)


# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are an Enterprise Business Intelligence Analyst.

Your job is to analyze structured business data.

You are NOT allowed to invent facts.

Everything you write MUST come directly from
the supplied business context.

If information is unavailable, say:

"Not enough information available."

Always respond in English.

Never translate column names.

Never change measurement units.

Never estimate values.

Never compare unrelated metrics.

Never generate business metrics that do not exist.

Recommendations MUST be supported by evidence.

Insights MUST describe observations.

Recommendations MUST describe actions.

Return ONLY valid JSON.

Never return Markdown.

Never return explanations.

Never return code blocks.

Use the KPIs as the primary source of truth.

Use the Business Analysis section to explain why the KPIs matter.

Use Trends only to describe changes over time.

Use Outliers only when they are statistically significant.

Do not repeat the same information across summary, insights, and recommendations.

Whenever numeric values are available in the supplied business context, include them inside the insight's data object.

Example:

{
    "key":"highest_average_stay",

    "description":"Cardiology has the highest average stay.",

    "data":{

        "department":"Cardiology",

        "average_stay":10.84,

        "unit":"days"

    }

}
"""

# ==========================================================
# Dataset Instructions
# ==========================================================

DATASET_INSTRUCTIONS = {

    "retail": """
Focus on:

• Sales
• Profit
• Products
• Customers
• Categories
• Regional performance
• Profitability

Do not discuss hospitals,
patients,
finance,
or education.
""",

    "hospital": """
Focus on:

• Patients
• Departments
• Bills
• Length of stay
• Doctors
• Age distribution

DaysAdmitted is measured in DAYS.

Never convert days to weeks, months,
or years.

Bill values represent currency.

Never convert currency into percentages.

Department names must remain unchanged.
Bill represents MONEY.

Never convert days into years.
""",

    "finance": """
Focus on:

• Revenue
• Expenses
• Net Profit
• Cost
• Financial trends

Never discuss products,
patients,
or students.
""",

    "hr": """
Focus on:

• Employees
• Salary
• Department
• Designation
• Workforce statistics

Never discuss revenue,
patients,
or sales.
""",

    "education": """
Focus on:

• Students
• Marks
• Grades
• Subjects
• Academic performance

Never discuss customers,
sales,
or hospital metrics.
""",

    "generic": """
Analyze only the supplied dataset.

Do not assume the business domain.

Use only available metrics.
"""
}


# ==========================================================
# JSON Output Schema
# ==========================================================

OUTPUT_SCHEMA = {

    "summary": "string",

    "confidence": 0.95,

    "insights": [

        {

            "key":"string",

            "description":"string",

            "data":{

                "metric":"value"

            }

        }

    ],

    "recommendations":[

        {

            "key":"string",

            "description":"string",

            "priority":"high"

        }

    ],

    "charts":[

        {

            "type":"bar",

            "title":"string",

            "reason":"string"

        }

    ],

    "warnings":[

    ]

}


# ==========================================================
# Validation Rules
# ==========================================================

VALIDATION_RULES = """
Before returning the response verify:

1. Response is valid JSON.

2. Response is entirely in English.

3. Summary contains fewer than
   80 words.

4. Confidence is between
   0.0 and 1.0.

5. Every insight must contain:

   key

   description

   data

6. Every recommendation must contain:

   key

   description

   priority

7. Every insight data object must contain
   supporting business values.

8. Every fact must exist in the supplied
   business context.

9. Never invent KPIs.

10. Never rename metrics.

11. Preserve measurement units.

12. Never compare unrelated values.

13. Charts must contain:

    type

    title

    reason

14. Warnings must always exist.

Return [] if none.

15. Confidence must always exist.

16. Return ONLY valid JSON.
"""

# ==========================================================
# Safe Serialization
# ==========================================================

def to_pretty_json(data: Any) -> str:
    """
    Safely serialize Python objects into formatted JSON.

    Returns "{}" if serialization fails.
    """

    try:
        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    except Exception:

        return "{}"


# ==========================================================
# Context Helpers
# ==========================================================

def get_context(
    context: Dict[str, Any],
    key: str
) -> Any:
    """
    Safely retrieve a value from context.

    Returns an empty dictionary if the key
    does not exist.
    """

    return context.get(key, {})


def get_dataset_type(
    context: Dict[str, Any]
) -> str:
    """
    Returns detected dataset type.

    Defaults to generic.
    """

    dataset = str(

        context.get(
            "dataset_type",
            "generic"
        )

    ).lower()

    if dataset not in SUPPORTED_DATASETS:

        dataset = "generic"

    return dataset


# ==========================================================
# Prompt Sections
# ==========================================================

def build_user_query(
    query: str
) -> str:
    """
    User question section.
    """

    return f"""
==================================================
USER QUESTION
==================================================

{query.strip()}
"""


def build_dataset_section(
    dataset_type: str
) -> str:
    """
    Dataset type section.
    """

    instructions = DATASET_INSTRUCTIONS.get(
        dataset_type,
        DATASET_INSTRUCTIONS["generic"]
    )

    return f"""
==================================================
DATASET TYPE
==================================================

{dataset_type.upper()}

==================================================
DATASET GUIDELINES
==================================================

{instructions}
"""


def build_json_section(
    title: str,
    data: Any
) -> str:
    """
    Generic JSON block.

    Used for KPIs,
    statistics,
    business analysis,
    trends,
    etc.
    """

    return f"""
==================================================
{title}
==================================================

{to_pretty_json(data)}
"""


# ==========================================================
# Business Context Optimizer
# ==========================================================

def optimize_business_context(
    business: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Reduce unnecessary prompt size.

    Removes very large sections that
    are not always useful for LLM
    reasoning.

    This keeps token usage lower.
    """

    if not business:

        return {}

    optimized = dict(business)

    # Large matrices are rarely useful
    optimized.pop("correlations", None)

    # Very verbose summaries
    optimized.pop("numeric_analysis", None)

    optimized.pop("categorical_analysis", None)

    return optimized


# ==========================================================
# Prompt Context
# ==========================================================

def prepare_context(
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract every component required
    by the prompt builder.
    """

    business = optimize_business_context(

        get_context(
            context,
            "business"
        )

    )

    return {

        "query":

            context.get(
                "query",
                "Analyze the supplied dataset."
            ),

        "dataset_type":

            get_dataset_type(
                context
            ),

        "profile":

            get_context(
                context,
                "profile"
            ),

        "kpis":

            get_context(
                context,
                "kpis"
            ),

        "statistics":

            get_context(
                context,
                "statistics"
            ),

        "business":

            business,

        "trends":

            get_context(
                context,
                "trends"
            ),

        "outliers":

            get_context(
                context,
                "outliers"
            )
    }


# ==========================================================
# Prompt Rules
# ==========================================================

def build_rules_section() -> str:
    """
    Common prompt rules.

    These rules dramatically reduce
    hallucinations.
    """

    return """
==================================================
STRICT RULES
==================================================

Use ONLY the supplied business context.

Never invent numbers.

Never estimate values.

Never calculate new KPIs.

Never rename metrics.

Never compare unrelated metrics.

Never change measurement units.

Never convert days into years.

Never convert currency into percentages.

Every insight MUST contain a populated data object.

Never leave the data object empty.

Copy numeric values exactly as supplied.

Do not summarize numbers without including them
inside the data object.

Generate exactly three chart recommendations.

If there are no warnings,
return an empty array.

Do not omit confidence.

Return confidence as a decimal
between 0 and 1.

If information is missing,
explicitly state:

"Not enough information available."

Do not mention data that does not exist.
"""

# ==========================================================
# Output Schema Section
# ==========================================================

def build_output_schema() -> str:
    """
    Returns the required JSON schema that the
    LLM must strictly follow.
    """

    return f"""
==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

No Markdown.

No explanations.

No comments.

No code blocks.

The response MUST exactly follow
this schema.

{to_pretty_json(OUTPUT_SCHEMA)}
"""


# ==========================================================
# Validation Section
# ==========================================================

def build_validation_section() -> str:
    """
    Final validation checklist.
    """

    return f"""
==================================================
VALIDATION
==================================================

{VALIDATION_RULES}
"""


# ==========================================================
# Build Prompt
# ==========================================================

def build_prompt(
    context: Dict[str, Any]
) -> str:
    """
    Build the complete DeepSeek prompt.

    Parameters
    ----------
    context

        Dictionary containing:

        query

        dataset_type

        profile

        kpis

        statistics

        business

        trends

        outliers

    Returns
    -------
    Complete prompt string.
    """

    prepared = prepare_context(
        context
    )

    sections = [

        SYSTEM_PROMPT,

        build_user_query(
            prepared["query"]
        ),

        build_dataset_section(
            prepared["dataset_type"]
        ),

        build_json_section(
            "DATASET PROFILE",
            prepared["profile"]
        ),

        build_json_section(
            "BUSINESS KPIs",
            prepared["kpis"]
        ),

        build_json_section(
            "STATISTICS",
            prepared["statistics"]
        ),

        build_json_section(
            "BUSINESS ANALYSIS",
            prepared["business"]
        ),

        build_json_section(
            "TREND ANALYSIS",
            prepared["trends"]
        ),

        build_json_section(
            "OUTLIERS",
            prepared["outliers"]
        ),

        build_rules_section(),

        build_output_schema(),

        build_validation_section()

    ]

    return "\n".join(sections)

