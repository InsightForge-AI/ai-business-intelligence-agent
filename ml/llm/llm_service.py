"""
==========================================================
LLM Service
==========================================================

Author:
    AI Business Intelligence Agent

Purpose
-------
Orchestrates the complete LLM workflow.

Responsibilities
----------------
• Validate context
• Build prompt
• Call DeepSeek
• Parse response
• Measure latency
• Return standardized response
"""

from __future__ import annotations

import time

from typing import Any, Dict

from llm.prompts import build_prompt
from llm.deepseek import (
    generate,
    MODEL_NAME,
)
from llm.parser import (
    parse_response,
    build_default_response
)


# ==========================================================
# Response Envelope
# ==========================================================

def build_response(
    *,
    success: bool,
    response: Dict[str, Any],
    latency: float = 0.0,
    error: str = ""
) -> Dict[str, Any]:
    """
    Build the standardized service response.
    """

    return {

        "success": success,

        "model": MODEL_NAME,

        "latency": round(
            latency,
            3
        ),

        "error": error,

        "response": response

    }


# ==========================================================
# Context Validation
# ==========================================================

REQUIRED_FIELDS = {

    "query",

    "profile",

    "kpis",

    "statistics",

    "business",

    "trends",

    "outliers"

}


def validate_context(
    context: Dict[str, Any]
) -> None:
    """
    Validate the context passed to the LLM.

    Raises
    ------
    ValueError
        If required fields are missing.
    """

    if not isinstance(
        context,
        dict
    ):
        raise ValueError(
            "Context must be a dictionary."
        )

    missing = [

        field

        for field in REQUIRED_FIELDS

        if field not in context

    ]

    if missing:

        raise ValueError(

            "Missing required context fields: "

            + ", ".join(missing)

        )


# ==========================================================
# Timer Helpers
# ==========================================================

def start_timer() -> float:
    """
    Start latency timer.
    """

    return time.perf_counter()


def stop_timer(
    start: float
) -> float:
    """
    Stop latency timer.
    """

    return time.perf_counter() - start

# ==========================================================
# Prompt Builder
# ==========================================================

def build_llm_prompt(
    context: Dict[str, Any]
) -> str:
    """
    Validate the context and build the prompt.
    """

    validate_context(
        context
    )

    return build_prompt(
        context
    )


# ==========================================================
# LLM Call
# ==========================================================

async def call_llm(
    prompt: str
) -> str:
    """
    Execute the LLM request.

    Returns
    -------
    Raw model response.

    Raises
    ------
    RuntimeError
        If the model returns an invalid response.
    """

    response = await generate(
        prompt
    )

    if response is None:

        raise RuntimeError(
            "LLM returned None."
        )

    response = str(
        response
    ).strip()

    if not response:

        raise RuntimeError(
            "LLM returned an empty response."
        )

    return response


# ==========================================================
# Parse LLM Response
# ==========================================================

def parse_llm_response(
    response: str
) -> Dict[str, Any]:
    """
    Parse the raw LLM response into the
    standardized schema.
    """

    parsed = parse_response(
        response
    )

    if not isinstance(
        parsed,
        dict
    ):

        raise RuntimeError(
            "Parser returned an invalid object."
        )

    return parsed


# ==========================================================
# Prompt Stage
# ==========================================================

def execute_prompt_stage(
    context: Dict[str, Any]
) -> str:
    """
    Build the prompt.

    This stage isolates prompt generation
    failures from LLM failures.
    """

    try:

        return build_llm_prompt(
            context
        )

    except Exception as exc:

        raise RuntimeError(

            f"Prompt generation failed: {exc}"

        ) from exc


# ==========================================================
# LLM Stage
# ==========================================================

async def execute_llm_stage(
    prompt: str
) -> str:
    """
    Execute the model.

    This stage isolates inference failures.
    """

    try:

        return await call_llm(
            prompt
        )

    except Exception as exc:

        raise RuntimeError(

            f"LLM execution failed: {exc}"

        ) from exc


# ==========================================================
# Parser Stage
# ==========================================================

def execute_parser_stage(
    response: str
) -> Dict[str, Any]:
    """
    Execute the parser.

    Keeps parser failures isolated.
    """

    try:

        return parse_llm_response(
            response
        )

    except Exception as exc:

        raise RuntimeError(

            f"Parser failed: {exc}"

        ) from exc
    
# ==========================================================
# Main Service
# ==========================================================

async def generate_insights(
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate AI-powered business insights.

    Pipeline
    --------
    Validate Context
            ↓
    Build Prompt
            ↓
    Call LLM
            ↓
    Parse Response
            ↓
    Return Standardized Result
    """

    timer = start_timer()

    try:

        # ----------------------------------------------
        # Prompt Stage
        # ----------------------------------------------

        prompt = execute_prompt_stage(
            context
        )

        # ----------------------------------------------
        # LLM Stage
        # ----------------------------------------------

        raw_response = await execute_llm_stage(
            prompt
        )

        # ----------------------------------------------
        # Parser Stage
        # ----------------------------------------------

        parsed_response = execute_parser_stage(
            raw_response
        )

        latency = stop_timer(
            timer
        )

        return build_response(

            success=True,

            response=parsed_response,

            latency=latency

        )

    except Exception as exc:

        latency = stop_timer(
            timer
        )

        fallback = build_default_response()

        fallback["warnings"].append(
            str(exc)
        )

        return build_response(

            success=False,

            response=fallback,

            latency=latency,

            error=str(exc)

        )
    
# ==========================================================
# Convenience Alias
# ==========================================================

async def run(
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convenience alias.

    Example
    -------
        result = await run(context)
    """

    return await generate_insights(
        context
    )


# ==========================================================
# Health Check
# ==========================================================

def service_info() -> Dict[str, Any]:
    """
    Return service metadata.

    Useful for diagnostics.
    """

    return {

        "service": "LLM Service",

        "model": MODEL_NAME,

        "status": "ready"

    }


# ==========================================================
# Public API
# ==========================================================

__all__ = [

    "generate_insights",

    "run",

    "service_info",

    "build_response"

]