from fastapi import APIRouter
from schemas.request_schema import QueryRequest, AnalyzeResponse
from services.decision_service import decide

router = APIRouter()


@router.post(
    "/agent/analyze",
    response_model=AnalyzeResponse,
    response_model_exclude_none=True
)
def analyze(request: QueryRequest) -> AnalyzeResponse:
    try:
        # Empty query fallback
        if not request.query or not request.query.strip():
            return AnalyzeResponse(
                status="success",
                query=request.query,
                modules=["nlp"],
                confidence=0.0,
                message="Empty query received. Defaulting to NLP."
            )

        # Decision engine
        result = decide(request.query)

        # Safety validation
        if (
            not result
            or not isinstance(result, dict)
            or "modules" not in result
        ):
            result = {
                "modules": ["nlp"],
                "confidence": 0.0
            }

        return AnalyzeResponse(
            status="success",
            query=request.query,
            modules=result["modules"],
            confidence=result["confidence"]
        )

    except Exception as e:
        print(e)

    return AnalyzeResponse(
        status="error",
        query=request.query if request else "",
        modules=["nlp"],
        confidence=0.0,
        message="Unexpected error. Defaulting to NLP."
    )