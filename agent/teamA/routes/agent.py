from fastapi import APIRouter, HTTPException
from schemas.models import AnalyzeRequest, AnalyzeResponse
from services.decision import decide

router = APIRouter()

@router.post("/agent/analyze", response_model=AnalyzeResponse)
def agent_analyze(request: AnalyzeRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Field 'query' must not be empty")
    return AnalyzeResponse(action=decide(request.query))
