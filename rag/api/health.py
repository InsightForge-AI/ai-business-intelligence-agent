"""
==========================================================
Health API
==========================================================

Health check endpoint.
"""

from fastapi import APIRouter

from utils.constants import (
    SERVICE_NAME,
    VERSION
)

router = APIRouter()


@router.get("/health")
async def health():
    """
    Service health.
    """

    return {

        "service": SERVICE_NAME,

        "version": VERSION,

        "status": "healthy"

    }