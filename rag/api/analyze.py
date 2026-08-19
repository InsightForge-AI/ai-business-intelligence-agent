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