"""
==========================================================
Response Formatter
==========================================================

Author:
    AI Business Intelligence Agent

Purpose
-------
Format the final ML analysis result into the
standardized MLResponse model.
"""

from __future__ import annotations

from models.response import MLResponse


def format_response(
    analysis_result: dict
) -> MLResponse:
    """
    Format the final ML response.
    """

    # --------------------------------------------------
    # LLM Response
    # --------------------------------------------------

    llm_service = analysis_result.get(
        "llm",
        {}
    )

    llm = llm_service.get(
        "response",
        {}
    )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    success = llm_service.get(
        "success",
        True
    )

    message = (
        "Business analysis completed successfully."
        if success
        else "Business analysis failed."
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata = analysis_result.get(
        "metadata",
        {}
    )

    metadata.update({

        "model": llm_service.get(
            "model",
            ""
        ),

        "latency": llm_service.get(
            "latency",
            0.0
        )

    })

    # --------------------------------------------------
    # Build Response
    # --------------------------------------------------

    return MLResponse(

        # Module

        module="ml",

        success=success,

        # AI Response

        summary=llm.get(
            "summary",
            ""
        ),

        confidence=llm.get(
            "confidence",
            0.0
        ),

        insights=llm.get(
            "insights",
            []
        ),

        recommendations=llm.get(
            "recommendations",
            []
        ),

        # Business Data

        kpis=analysis_result.get(
            "kpis",
            {}
        ),

        charts=llm.get(
            "charts",
            []
        ),

        warnings=llm.get(
            "warnings",
            []
        ),

        metadata=metadata,

        # Message

        message=message

    )