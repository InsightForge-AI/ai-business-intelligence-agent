"""
==========================================================
DocuMind NLP Service
==========================================================

Main FastAPI application.
"""

from fastapi import FastAPI

from api.health import router as health_router
from api.routes import router as nlp_router

from utils.constants import (
    SERVICE_NAME,
    VERSION
)


app = FastAPI(

    title=SERVICE_NAME,

    version=VERSION,

    description="DocuMind NLP Microservice"

)

# ---------------------------------------------------------
# Register Routes
# ---------------------------------------------------------

app.include_router(

    health_router,

    tags=["Health"]

)

app.include_router(

    nlp_router,

    prefix="/nlp",

    tags=["NLP"]

)


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
async def root():
    """
    Root endpoint.
    """

    return {

        "service": SERVICE_NAME,

        "version": VERSION,

        "status": "running"

    }