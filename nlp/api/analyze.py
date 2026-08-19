"""
==========================================================
NLP Analysis API
==========================================================

Receives NLP analysis requests from the Backend.
"""

import traceback

from fastapi import APIRouter
from fastapi import HTTPException

from models.request import NLPRequest
from models.response import NLPResponse

from services.nlp_service import run_analysis


router = APIRouter()


@router.post(
    "/analyze",
    response_model=NLPResponse
)
async def analyze(
    request: NLPRequest
):
    """
    Execute NLP analysis.
    """

    try:

        response = await run_analysis(

            query=request.query,

            content=request.content,

            metadata=request.metadata

        )

        return response

    except Exception as e:

        print("\n========== NLP ERROR ==========")

        traceback.print_exc()

        print("===============================\n")

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )