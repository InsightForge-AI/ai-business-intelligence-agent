from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    query: str = Field(description="User query to route to the correct service")

class AnalyzeResponse(BaseModel):
    action: str = Field(description="Resolved service module: nlp, ml, cv, or unknown")
