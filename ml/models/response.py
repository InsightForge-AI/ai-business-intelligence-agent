"""
==========================================================
ML Response Model
==========================================================

Defines the standardized response returned
by the ML Service.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# Insight Model
# ==========================================================

class Insight(BaseModel):
    """
    Individual business insight.
    """

    key: str = Field(
        default="",
        description="Insight title"
    )

    description: Optional[str] = Field(
        default=None,
        description="Insight description"
    )

    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Supporting data"
    )


# ==========================================================
# Recommendation Model
# ==========================================================

class Recommendation(BaseModel):
    """
    Individual recommendation.
    """

    key: str = Field(
        default="",
        description="Recommendation title"
    )

    description: str = Field(
        default="",
        description="Recommendation description"
    )


# ==========================================================
# Metadata
# ==========================================================

class Metadata(BaseModel):
    """
    AI generation metadata.
    """

    model: str = Field(
        default="",
        description="LLM model used"
    )

    latency: float = Field(
        default=0.0,
        description="Inference latency in seconds"
    )


# ==========================================================
# ML Response
# ==========================================================

class MLResponse(BaseModel):
    """
    Standard ML Service Response.
    """

    module: str = Field(
        default="ml",
        description="Module name"
    )

    success: bool = Field(
        default=True,
        description="Analysis status"
    )

    summary: str = Field(
        default="",
        description="Business summary"
    )

    confidence: float = Field(
        default=0.0,
        description="LLM confidence score"
    )

    insights: List[Insight] = Field(
        default_factory=list,
        description="Generated business insights"
    )

    recommendations: List[Recommendation] = Field(
        default_factory=list,
        description="Business recommendations"
    )

    kpis: Dict[str, Any] = Field(
        default_factory=dict,
        description="Calculated KPIs"
    )

    charts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Chart configuration"
    )

    warnings: List[str] = Field(
        default_factory=list,
        description="Warnings generated during analysis"
    )

    metadata: Metadata = Field(
        default_factory=Metadata,
        description="LLM metadata"
    )

    message: str = Field(
        default="Analysis completed successfully.",
        description="Status message"
    )