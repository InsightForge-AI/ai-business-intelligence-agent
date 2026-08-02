"""
==========================================================
ML Pipeline
==========================================================

Author:
    AI Business Intelligence Agent

Purpose
-------
Coordinates the complete ML workflow.

Pipeline
--------
Load Dataset
        ↓
Generate Profile
        ↓
Business Analysis
        ↓
LLM Insights
        ↓
Format Response
"""

from __future__ import annotations

import logging

from analysis.loader import load_data
from analysis.profiler import generate_profile
from analysis.analysis import run_analysis
from analysis.formatter import format_response

from models.response import MLResponse

logger = logging.getLogger(__name__)


# ==========================================================
# ML Pipeline
# ==========================================================

async def run_pipeline(request) -> MLResponse:
    """
    Execute the complete ML pipeline.

    Parameters
    ----------
    request
        ML request containing:
            • content
            • query
            • metadata

    Returns
    -------
    MLResponse
        Standardized ML response.
    """

    try:

        # --------------------------------------------------
        # Validate Request
        # --------------------------------------------------

        if request is None:
            raise ValueError("Request cannot be None.")

        if getattr(request, "content", None) is None:
            raise ValueError("Dataset content is missing.")

        logger.info("Starting ML pipeline.")

        # --------------------------------------------------
        # Load Dataset
        # --------------------------------------------------

        logger.info("Loading dataset...")

        dataframe = load_data(
            request.content
        )

        # --------------------------------------------------
        # Generate Dataset Profile
        # --------------------------------------------------

        logger.info("Generating dataset profile...")

        profile = generate_profile(
            dataframe
        )

        # --------------------------------------------------
        # Run Business Analysis
        # --------------------------------------------------

        logger.info("Running business analysis...")

        analysis_result = await run_analysis(

            dataframe=dataframe,

            query=getattr(
                request,
                "query",
                ""
            ),

            metadata=getattr(
                request,
                "metadata",
                {}
            ),

            profile=profile

        )

        # --------------------------------------------------
        # Format Response
        # --------------------------------------------------

        logger.info("Formatting response...")

        response = format_response(
            analysis_result
        )

        logger.info("ML pipeline completed successfully.")

        return response

    except Exception as exc:

        logger.exception(
            "ML pipeline failed."
        )

        return MLResponse(

            module="ml",

            success=False,

            message=f"Pipeline execution failed: {exc}"

        )


# ==========================================================
# Public API
# ==========================================================

__all__ = [

    "run_pipeline"

]