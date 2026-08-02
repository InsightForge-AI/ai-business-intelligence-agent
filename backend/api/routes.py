"""
==========================================================
Backend Routes
==========================================================

Registers all Backend API endpoints.
"""

from fastapi import APIRouter


from api.health import router as health_router

from api.upload import router as upload_router

from api.analyze import router as analyze_router

from api.dashboard import router as dashboard_router

from api.summary import router as summary_router

from api.documents import router as documents_router

from api.preview import router as preview_router

from api.rename import router as rename_router

from api.delete import router as delete_router

from api.download import router as download_router





router = APIRouter(

    prefix="/api"

)





# ---------------------------------------------------------
# Health APIs
# ---------------------------------------------------------

router.include_router(

    health_router,

    tags=["Health"]

)





# ---------------------------------------------------------
# Upload APIs
# ---------------------------------------------------------

router.include_router(

    upload_router,

    tags=["Upload"]

)





# ---------------------------------------------------------
# Dashboard APIs
# ---------------------------------------------------------

router.include_router(

    dashboard_router,

    tags=["Dashboard"]

)





# ---------------------------------------------------------
# Analyze APIs
# ---------------------------------------------------------

router.include_router(

    analyze_router,

    tags=["Analyze"]

)





# ---------------------------------------------------------
# Summary APIs
# ---------------------------------------------------------

router.include_router(

    summary_router,

    tags=["Summary"]

)





# ---------------------------------------------------------
# Documents APIs
# ---------------------------------------------------------

router.include_router(

    documents_router,

    tags=["Documents"]

)





# ---------------------------------------------------------
# Preview APIs
# ---------------------------------------------------------

router.include_router(

    preview_router,

    tags=["Preview"]

)





# ---------------------------------------------------------
# Rename APIs
# ---------------------------------------------------------

router.include_router(

    rename_router,

    tags=["Rename"]

)





# ---------------------------------------------------------
# Delete APIs
# ---------------------------------------------------------

router.include_router(

    delete_router,

    tags=["Delete"]

)





# ---------------------------------------------------------
# Download APIs
# ---------------------------------------------------------

router.include_router(

    download_router,

    tags=["Download"]

)