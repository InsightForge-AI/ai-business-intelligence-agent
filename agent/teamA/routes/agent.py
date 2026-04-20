from fastapi import APIRouter, HTTPException

from ..schemas.models import AnalyzeRequest, AnalyzeResponse
from ..services.decision import decide_modules

router = APIRouter()


def _format_actions(actions: list[str]) -> AnalyzeResponse:
    if len(actions) == 1:
        return actions[0]
    return actions


@router.post("/agent/analyze", response_model=AnalyzeResponse)
def agent_analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Field 'query' must not be empty")

    try:
        actions = decide_modules(request.query)
        return _format_actions(actions)
    except Exception:
        # Sprint 3 requirement: never crash on valid input, use NLP as safe fallback.
        return "nlp"
