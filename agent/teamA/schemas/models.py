from typing import Union

from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    query: str = Field(description="User query to route to the correct service")

AnalyzeResponse = Union[str, list[str]]
