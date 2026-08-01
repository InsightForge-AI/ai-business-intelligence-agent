"""
==========================================================
Health API
==========================================================

Provides health status of the
Agent service.
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
    Health check endpoint.
    """

    return {

        "module": MODULE_NAME,

        "service": SERVICE_NAME,

        "version": VERSION,

        "status": "healthy"

    }