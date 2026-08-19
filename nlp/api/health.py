"""
==========================================================
NLP Health API
==========================================================

Health check endpoint.
"""

from fastapi import APIRouter

from utils.constants import (
    MODULE_NAME,
    SERVICE_NAME,
    VERSION
)


router = APIRouter()


@router.get("/health")
async def health():
    """
    Health endpoint.
    """

    return {

        "module": MODULE_NAME,

        "service": SERVICE_NAME,

        "version": VERSION,

        "status": "healthy"

    }