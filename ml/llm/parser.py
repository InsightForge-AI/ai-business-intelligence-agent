"""
==========================================================
LLM Response Parser
==========================================================

Author:
    AI Business Intelligence Agent

Purpose
-------
Parse, validate and normalize responses returned
by Large Language Models.

Responsibilities
----------------
• Remove thinking blocks
• Remove Markdown
• Extract JSON
• Repair malformed JSON
• Validate schema
• Normalize response
• Apply default values
• Return consistent Python dictionary
"""

from __future__ import annotations

import json
import re

from typing import Any, Dict


# ==========================================================
# Configuration
# ==========================================================

DEFAULT_CONFIDENCE = 0.95

DEFAULT_PRIORITY = "medium"

VALID_PRIORITIES = {
    "low",
    "medium",
    "high"
}


# ==========================================================
# Default Response
# ==========================================================

DEFAULT_RESPONSE = {

    "summary": "",

    "confidence": DEFAULT_CONFIDENCE,

    "insights": [],

    "recommendations": [],

    "charts": [],

    "warnings": []

}


# ==========================================================
# Safe Helpers
# ==========================================================

def safe_string(
    value: Any
) -> str:
    """
    Safely convert a value to string.
    """

    if value is None:

        return ""

    return str(value).strip()


def safe_float(
    value: Any,
    default: float = DEFAULT_CONFIDENCE
) -> float:
    """
    Safely convert a value to float.
    """

    try:

        value = float(value)

        if value < 0:
            return 0.0

        if value > 1:
            return 1.0

        return round(value, 3)

    except Exception:

        return default


# ==========================================================
# Empty Structures
# ==========================================================

def empty_insight() -> Dict[str, Any]:
    """
    Default insight object.
    """

    return {

        "key": "",

        "description": "",

        "data": {}

    }


def empty_recommendation() -> Dict[str, Any]:
    """
    Default recommendation object.
    """

    return {

        "key": "",

        "description": "",

        "priority": DEFAULT_PRIORITY

    }


def empty_chart() -> Dict[str, Any]:
    """
    Default chart object.
    """

    return {

        "type": "",

        "title": "",

        "reason": ""

    }


# ==========================================================
# Build Default Response
# ==========================================================

def build_default_response() -> Dict[str, Any]:
    """
    Return an empty normalized response.
    """

    return {

        "summary": "",

        "confidence": DEFAULT_CONFIDENCE,

        "insights": [],

        "recommendations": [],

        "charts": [],

        "warnings": []

    }


# ==========================================================
# Normalize Lists
# ==========================================================

def normalize_list(
    items: Any
) -> list:
    """
    Convert arbitrary values into lists.
    """

    if items is None:

        return []

    if isinstance(items, list):

        return items

    return [items]


# ==========================================================
# Normalize Priority
# ==========================================================

def normalize_priority(
    priority: Any
) -> str:
    """
    Normalize recommendation priority.
    """

    priority = safe_string(
        priority
    ).lower()

    if priority not in VALID_PRIORITIES:

        return DEFAULT_PRIORITY

    return priority

# ==========================================================
# Response Cleaning
# ==========================================================

def remove_thinking_blocks(
    response: str
) -> str:
    """
    Remove <think>...</think> sections produced by
    reasoning models.
    """

    return re.sub(
        r"<think>[\s\S]*?</think>",
        "",
        response,
        flags=re.IGNORECASE
    )


def remove_markdown(
    response: str
) -> str:
    """
    Remove Markdown code fences.
    """

    response = re.sub(
        r"```json",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"```",
        "",
        response
    )

    return response.strip()


def normalize_quotes(
    response: str
) -> str:
    """
    Replace smart quotes with standard quotes.
    """

    replacements = {

        "“": "\"",

        "”": "\"",

        "‘": "'",

        "’": "'",

        "´": "'",

        "`": "'"

    }

    for source, target in replacements.items():

        response = response.replace(
            source,
            target
        )

    return response


def remove_control_characters(
    response: str
) -> str:
    """
    Remove invisible control characters.
    """

    return re.sub(
        r"[\x00-\x1F]",
        "",
        response
    )


def clean_response(
    response: str
) -> str:
    """
    Execute every cleaning step.
    """

    response = remove_thinking_blocks(
        response
    )

    response = remove_markdown(
        response
    )

    response = normalize_quotes(
        response
    )

    response = remove_control_characters(
        response
    )

    return response.strip()


# ==========================================================
# JSON Extraction
# ==========================================================

def extract_json(
    response: str
) -> str:
    """
    Extract the first complete JSON object using
    balanced brace matching.

    This is safer than a greedy regex because
    LLMs often include explanatory text before
    or after the JSON.
    """

    start = response.find("{")

    if start == -1:

        return ""

    depth = 0

    for index in range(start, len(response)):

        character = response[index]

        if character == "{":

            depth += 1

        elif character == "}":

            depth -= 1

            if depth == 0:

                return response[start:index + 1]

    return ""


# ==========================================================
# JSON Repair
# ==========================================================

def repair_json(
    text: str
) -> str:
    """
    Repair common JSON formatting issues.
    """

    if not text:

        return ""

    # Remove trailing commas

    text = re.sub(

        r",(\s*[}\]])",

        r"\1",

        text

    )

    # Replace Python literals

    text = text.replace(
        "None",
        "null"
    )

    text = text.replace(
        "True",
        "true"
    )

    text = text.replace(
        "False",
        "false"
    )

    # Remove BOM

    text = text.replace(
        "\ufeff",
        ""
    )

    return text.strip()


# ==========================================================
# Safe JSON Loader
# ==========================================================

def safe_load_json(
    json_text: str
) -> Dict[str, Any]:
    """
    Safely deserialize JSON.

    Returns an empty dictionary on failure.
    """

    if not json_text:

        return {}

    try:

        return json.loads(
            json_text
        )

    except Exception:

        return {}
    
# ==========================================================
# Insight Normalization
# ==========================================================

def normalize_insights(
    insights: Any
) -> list:
    """
    Normalize insight objects.
    """

    normalized = []

    for item in normalize_list(insights):

        # Plain text insight
        if isinstance(item, str):

            normalized.append({

                "key": "",

                "description": safe_string(item),

                "data": {}

            })

            continue

        if not isinstance(item, dict):
            continue

        # Backward compatibility
        data = item.get("data")

        if data is None:
            data = item.get("evidence", {})

        if not isinstance(data, dict):
            data = {}

        normalized.append({

            "key": safe_string(
                item.get("key")
            ),

            "description": safe_string(
                item.get("description")
            ),

            "data": data

        })

    return normalized


# ==========================================================
# Recommendation Normalization
# ==========================================================

def normalize_recommendations(
    recommendations: Any
) -> list:
    """
    Normalize recommendation objects.
    """

    normalized = []

    for item in normalize_list(recommendations):

        if isinstance(item, str):

            normalized.append({

                "key": "",

                "description": safe_string(item),

                "priority": DEFAULT_PRIORITY

            })

            continue

        if not isinstance(item, dict):

            continue

        normalized.append({

            "key": safe_string(
                item.get("key")
            ),

            "description": safe_string(
                item.get("description")
            ),

            "priority": normalize_priority(
                item.get("priority")
            )

        })

    return normalized

# ==========================================================
# Supported Chart Types
# ==========================================================

VALID_CHART_TYPES = {

    "bar",
    "line",
    "pie",
    "scatter",
    "histogram",
    "area",
    "box"

}


# ==========================================================
# Chart Normalization
# ==========================================================

def normalize_charts(
    charts: Any
) -> list:
    """
    Normalize chart suggestions.

    Ensures every chart contains:
    • type
    • title
    • reason

    Invalid or unknown chart types default to "bar".
    """

    normalized = []

    for chart in normalize_list(charts):

        if not isinstance(chart, dict):
            continue

        chart_type = safe_string(
            chart.get("type")
        ).lower()

        if chart_type not in VALID_CHART_TYPES:
            chart_type = "bar"

        normalized.append({

            "type": chart_type,

            "title": safe_string(
                chart.get("title")
            ),

            "reason": safe_string(
                chart.get("reason")
            )

        })

    return normalized


# ==========================================================
# Warning Normalization
# ==========================================================

def normalize_warnings(
    warnings: Any
) -> list:
    """
    Normalize warning messages.
    """

    result = []

    for warning in normalize_list(warnings):

        warning = safe_string(warning)

        if warning:

            result.append(warning)

    return result


# ==========================================================
# Schema Validation
# ==========================================================

def validate_schema(
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Ensure required top-level fields exist.
    """

    if not isinstance(data, dict):

        return build_default_response()

    validated = build_default_response()

    validated["summary"] = safe_string(
        data.get("summary")
    )

    validated["confidence"] = safe_float(
        data.get("confidence")
    )

    validated["insights"] = normalize_insights(
        data.get("insights")
    )

    validated["recommendations"] = normalize_recommendations(
        data.get("recommendations")
    )

    validated["charts"] = normalize_charts(
        data.get("charts")
    )

    validated["warnings"] = normalize_warnings(
        data.get("warnings")
    )

    return validated


# ==========================================================
# Normalize Response
# ==========================================================

def normalize_response(
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Final normalization stage.

    Guarantees that every response returned by the parser
    matches the expected schema.
    """

    return validate_schema(data)

# ==========================================================
# Parse Response
# ==========================================================

def parse_response(
    response: str
) -> Dict[str, Any]:
    """
    Parse an LLM response into a validated Python dictionary.

    Pipeline
    --------
    Raw Response
        ↓
    Clean Response
        ↓
    Extract JSON
        ↓
    Repair JSON
        ↓
    Load JSON
        ↓
    Validate Schema
        ↓
    Normalize Response
        ↓
    Return Dictionary
    """

    # ------------------------------------------------------
    # Empty Response
    # ------------------------------------------------------

    if not response:

        result = build_default_response()

        result["warnings"].append(
            "Empty response received from LLM."
        )

        return result

    # ------------------------------------------------------
    # Clean Response
    # ------------------------------------------------------

    cleaned = clean_response(
        response
    )

    if not cleaned:

        result = build_default_response()

        result["warnings"].append(
            "Response became empty after cleaning."
        )

        return result

    # ------------------------------------------------------
    # Extract JSON
    # ------------------------------------------------------

    json_text = extract_json(
        cleaned
    )

    # ------------------------------------------------------
    # No JSON Found
    # ------------------------------------------------------

    if not json_text:

        result = build_default_response()

        result["summary"] = cleaned

        result["warnings"].append(
            "Structured JSON not found. Using plain text summary."
        )

        return result

    # ------------------------------------------------------
    # Repair JSON
    # ------------------------------------------------------

    json_text = repair_json(
        json_text
    )

    # ------------------------------------------------------
    # Deserialize
    # ------------------------------------------------------

    data = safe_load_json(
        json_text
    )

    # ------------------------------------------------------
    # Invalid JSON
    # ------------------------------------------------------

    if not data:

        result = build_default_response()

        result["summary"] = cleaned

        result["warnings"].append(
            "Unable to parse JSON response."
        )

        return result

    # ------------------------------------------------------
    # Validate
    # ------------------------------------------------------

    validated = validate_schema(
        data
    )

    # ------------------------------------------------------
    # Normalize
    # ------------------------------------------------------

    normalized = normalize_response(
        validated
    )

    return normalized


# ==========================================================
# Parse Alias
# ==========================================================

def parse(
    response: str
) -> Dict[str, Any]:
    """
    Convenience wrapper.

    Allows callers to simply use:

        parser.parse(response)
    """

    return parse_response(
        response
    )

# ==========================================================
# Validation Helpers
# ==========================================================

def is_valid_response(
    response: Dict[str, Any]
) -> bool:
    """
    Verify that the parsed response follows the
    expected schema.
    """

    if not isinstance(response, dict):
        return False

    required = {

        "summary": str,
        "confidence": (int, float),
        "insights": list,
        "recommendations": list,
        "charts": list,
        "warnings": list,

    }

    for key, expected_type in required.items():

        if key not in response:
            return False

        if not isinstance(
            response[key],
            expected_type
        ):
            return False

    return True


# ==========================================================
# Parse With Validation
# ==========================================================

def parse_and_validate(
    response: str
) -> Dict[str, Any]:
    """
    Parse the LLM response and ensure that the
    returned object always satisfies the schema.
    """

    parsed = parse_response(
        response
    )

    if not is_valid_response(
        parsed
    ):

        fallback = build_default_response()

        fallback["warnings"].append(
            "Parser returned an invalid response."
        )

        return fallback

    return parsed


# ==========================================================
# Public API
# ==========================================================

__all__ = [

    "parse",

    "parse_response",

    "parse_and_validate",

    "is_valid_response",

    "build_default_response"

]