from fastapi import APIRouter, HTTPException

from ..schemas.models import AnalyzeRequest, AnalyzeResponse
from ..services.decision import decide

router = APIRouter()

@router.post("/agent/analyze", response_model=AnalyzeResponse)
def agent_analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Field 'query' must not be empty")

    try:
        return AnalyzeResponse(action=decide(request.query))
    except Exception:
        # Sprint 3 requirement: never crash on valid input, use NLP as safe fallback.
        return AnalyzeResponse(action="nlp")
