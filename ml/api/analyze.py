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

        print("=" * 80)
        print("ML REQUEST RECEIVED")
        print("=" * 80)
        print(request.model_dump())

        # --------------------------------------------------
        # Load Dataset
        # --------------------------------------------------

        dataframe = load_data(request.content)

        print("Dataset Loaded")
        print(dataframe.head())

        # --------------------------------------------------
        # Generate Profile
        # --------------------------------------------------

        profile = generate_profile(dataframe)

        print("Profile Generated")
        print(profile)

        # --------------------------------------------------
        # Business Analysis
        # --------------------------------------------------

        analysis_result = await run_analysis(

            dataframe=dataframe,

            query=request.query,

            metadata=request.metadata,

            profile=profile

        )

        print("Analysis Completed")

        # --------------------------------------------------
        # Format Response
        # --------------------------------------------------

        response = format_response(
            analysis_result
        )

        print("Response Ready")

        return response

    except Exception as e:

        print("=" * 80)
        print("ML SERVICE ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )