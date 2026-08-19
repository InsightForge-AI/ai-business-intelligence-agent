"""
==========================================================
NLP Routes
==========================================================

Register all NLP API routes.
"""

from fastapi import APIRouter

from api.analyze import router as analyze_router


router = APIRouter()

router.include_router(

    analyze_router

)