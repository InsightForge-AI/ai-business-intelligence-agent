"""
==========================================================
ML Health API
==========================================================

Health check endpoints for the ML Service.
"""

from datetime import datetime

from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
async def health():
    """
    General health check.
    """

    return {

        "service": "DocuMind ML Service",

        "status": "healthy",

        "version": "1.0.0",

        "timestamp": datetime.utcnow().isoformat()

    }


@router.get("/health/live")
async def liveness():
    """
    Liveness Probe.
    """

    return {

        "status": "alive"

    }


@router.get("/health/ready")
async def readiness():
    """
    Readiness Probe.
    """

    return {

        "status": "ready",

        "llm": "DeepSeek",

        "service": "Machine Learning"

    }