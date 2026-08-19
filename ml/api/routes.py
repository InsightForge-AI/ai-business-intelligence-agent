"""
==========================================================
ML API Routes
==========================================================

Registers all API endpoints for the ML Service.
"""

from fastapi import APIRouter

from api.analyze import router as analyze_router
from api.health import router as health_router


router = APIRouter()


# ---------------------------------------------------------
# ML Analysis APIs
# ---------------------------------------------------------

router.include_router(

    analyze_router,

    prefix="/ml",

    tags=["Machine Learning"]

)


# ---------------------------------------------------------
# Health APIs
# ---------------------------------------------------------

router.include_router(

    health_router,

    tags=["Health"]

)