"""
==========================================================
Agent Routes
==========================================================

Registers all Agent API endpoints.
"""

from fastapi import APIRouter

from api.analyze import router as analyze_router


router = APIRouter()


# ---------------------------------------------------------
# Agent APIs
# ---------------------------------------------------------

router.include_router(

    analyze_router

)