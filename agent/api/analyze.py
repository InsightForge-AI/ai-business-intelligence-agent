"""
==========================================================
Agent Analysis API
==========================================================

Receives requests from the Backend and generates
an execution plan for downstream AI modules.

Workflow
--------
Backend
    ↓
Request Validation
    ↓
Agent Service
    ↓
Response
    ↓
Backend
"""

from fastapi import APIRouter
from fastapi import HTTPException

from models.request import AgentRequest
from models.response import AgentResponse

from services.agent_service import run_agent


router = APIRouter()


@router.post(
    "/analyze",
    response_model=AgentResponse
)
async def analyze(
    request: AgentRequest
):
    """
    Analyze the user request and generate
    an execution plan.
    """

    try:

        response = await run_agent(

            query=request.query,

            metadata=request.metadata

        )

        return response

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )