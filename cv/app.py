"""
==========================================================
CV Service
==========================================================

Computer Vision microservice for DocuMind.
"""

from fastapi import FastAPI

from api.routes import router as cv_router

from utils.constants import (
    SERVICE_NAME,
    VERSION
)


app = FastAPI(

    title=SERVICE_NAME,

    version=VERSION

)


app.include_router(

    cv_router,

    prefix="/cv",

    tags=[

        "Computer Vision"

    ]

)


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