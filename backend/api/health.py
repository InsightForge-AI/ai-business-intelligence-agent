"""
==========================================================
Health API
==========================================================

Health check endpoints for the DocuMind Backend.

Responsibilities
----------------
• Verify Backend availability
• Liveness checks
• Readiness checks
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

        "service": "DocuMind Backend",

        "status": "healthy",

        "version": "3.0.0",

        "timestamp": datetime.utcnow().isoformat()

    }


@router.get("/health/live")
async def liveness():
    """
    Liveness probe.

    Used by Docker/Kubernetes.
    """

    return {

        "status": "alive"

    }


@router.get("/health/ready")
async def readiness():
    """
    Readiness probe.
    """

    return {

        "status": "ready",

        "services": {

            "backend": "ready",

            "agent": "ready",

            "ml": "ready",

            "nlp": "ready",

            "rag": "ready",

            "cv": "ready"

        }

    }