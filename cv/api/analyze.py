"""
==========================================================
CV Analysis API
==========================================================

Receives Computer Vision analysis requests
from the Backend.
"""

import traceback

from fastapi import APIRouter
from fastapi import HTTPException

from models.request import CVRequest
from models.response import CVResponse

from services.cv_service import run_analysis


router = APIRouter()


@router.post(
    "/analyze",
    response_model=CVResponse
)
async def analyze(
    request: CVRequest
):
    """
    Execute Computer Vision analysis.
    """

    try:

        response = await run_analysis(

            query=request.query,

            content=request.content,

            metadata=request.metadata

        )

        return response

    except Exception as e:

        print("\n" + "=" * 60)
        print("CV SERVICE ERROR")
        print("=" * 60)

        traceback.print_exc()

        print("=" * 60 + "\n")

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )