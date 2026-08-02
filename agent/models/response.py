"""
==========================================================
Agent Response Model
==========================================================

Defines the response returned by
the Agent service to the Backend.
"""

from typing import List

from pydantic import BaseModel
from pydantic import Field


class AgentResponse(BaseModel):
    """
    Agent Analysis Response
    """

    module: str = Field(
        default="agent",
        description="Module name"
    )

    success: bool = Field(
        ...,
        description="Execution status"
    )

    intent: str = Field(
        ...,
        description="Detected user intent"
    )

    selected_modules: List[str] = Field(
        default_factory=list,
        description="Modules selected for execution"
    )

    execution_order: List[str] = Field(
        default_factory=list,
        description="Execution order of selected modules"
    )

    reason: str = Field(
        default="",
        description="Reason for module selection"
    )

    message: str = Field(
        default="Execution plan generated successfully.",
        description="Response message"
    )