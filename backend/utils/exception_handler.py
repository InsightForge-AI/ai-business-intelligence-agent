"""
==========================================================
Exception Handler
==========================================================

Responsibilities
----------------
• Return standardized error responses
"""

from fastapi.responses import JSONResponse


def error_response(
    message: str,
    status_code: int = 500
) -> JSONResponse:
    """
    Generate standardized error response.
    """

    return JSONResponse(

        status_code=status_code,

        content={

            "success": False,

            "status": "error",

            "message": message

        }

    )