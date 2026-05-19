from pydantic import BaseModel, Field
from typing import List, Optional


# Request schema
class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        description="User query for intelligent module routing",
        min_length=0
    )


# Response schema
class AnalyzeResponse(BaseModel):
    status: str = Field(
        description="Response status: success or error"
    )

    query: str = Field(
        description="Original user query"
    )

    modules: List[str] = Field(
        description="Selected modules for handling the query"
    )

    confidence: float = Field(
        description="Confidence score of routing decision"
    )

    message: Optional[str] = Field(
        default=None,
        description="Optional message for fallback or error handling"
    )