"""
==========================================================
RAG Analysis API
==========================================================

Receives RAG analysis requests from Backend.
"""

from fastapi import APIRouter
from fastapi import HTTPException

from models.request import RAGRequest
from models.response import RAGResponse

from services.rag_service import run_analysis


router = APIRouter()


@router.post("/analyze", response_model=RAGResponse)
async def analyze(request: RAGRequest):

    print("\n" + "=" * 80)
    print("RAG REQUEST")
    print("=" * 80)
    print("Query:", request.query)
    print("Content Length:", len(request.content))
    print("Content Preview:")
    print(request.content[:1000])
    print("Metadata:", request.metadata)
    print("=" * 80)

    try:
        response = await run_analysis(
            query=request.query,
            content=request.content,
            metadata=request.metadata
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )