"""
==========================================================
ML Analysis API
==========================================================

Receives requests from the Backend and executes
the complete ML pipeline.

Workflow
--------
Backend
    ↓
Request Validation
    ↓
Loader
    ↓
Profiler
    ↓
Business Analysis
    ↓
DeepSeek
    ↓
Formatter
    ↓
Backend
"""


import traceback

from fastapi import APIRouter, HTTPException

from models.request import MLRequest
from models.response import MLResponse

from analysis.loader import load_data
from analysis.profiler import generate_profile
from analysis.analysis import run_analysis
from analysis.formatter import format_response

router = APIRouter()


@router.post(
    "/analyze",
    response_model=MLResponse
)
async def analyze(request: MLRequest):
    """
    Analyze structured business data.
    """

    try:

        # --------------------------------------------------
        # Load Dataset
        # --------------------------------------------------

        dataframe = load_data(request.content)

        # --------------------------------------------------
        # Generate Profile
        # --------------------------------------------------

        profile = generate_profile(dataframe)

        # --------------------------------------------------
        # Business Analysis
        # --------------------------------------------------

        analysis_result = await run_analysis(

            dataframe=dataframe,

            query=request.query,

            metadata=request.metadata,

            profile=profile

        )

        # --------------------------------------------------
        # Format Response
        # --------------------------------------------------

        response = format_response(
            analysis_result
        )

        return response

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )