"""
==========================================================
CV Routes
==========================================================

Register all API routes.
"""

from fastapi import APIRouter

from api.health import router as health_router
from api.analyze import router as analyze_router


router = APIRouter()


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

router.include_router(

    health_router,

    tags=[

        "Health"

    ]

)

# ---------------------------------------------------------
# Analysis
# ---------------------------------------------------------

router.include_router(

    analyze_router,

    tags=[

        "Computer Vision"

    ]

)