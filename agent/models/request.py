"""
==========================================================
Agent Request Model
==========================================================

Defines the request schema received from
the Backend.
"""

from typing import Any
from typing import Dict

from pydantic import BaseModel
from pydantic import Field


class AgentRequest(BaseModel):
    """
    Agent Analysis Request
    """

    query: str = Field(
        ...,
        description="User query"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata"
    )