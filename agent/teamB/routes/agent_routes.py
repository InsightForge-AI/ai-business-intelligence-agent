from fastapi import APIRouter
from schemas.request_schema import QueryRequest
from services.decision_service import decide

router = APIRouter()

@router.post("/agent/analyze")
def analyze(request: QueryRequest):
    result = decide(request.query)
    return {"action": result}