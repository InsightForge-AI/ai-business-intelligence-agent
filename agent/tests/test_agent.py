"""
==========================================================
Agent Service Tests
==========================================================

Tests the complete Agent workflow.
"""

import pytest

from services.agent_service import run_agent


@pytest.mark.asyncio
async def test_business_analysis():

    response = await run_agent(

        query="Analyze the quarterly sales report.",

        metadata={

            "file_type": "pdf"

        }

    )

    assert response["success"] is True

    assert response["module"] == "agent"

    assert isinstance(

        response["intent"],

        str

    )

    assert isinstance(

        response["selected_modules"],

        list

    )

    assert isinstance(

        response["execution_order"],

        list

    )


@pytest.mark.asyncio
async def test_document_summary():

    response = await run_agent(

        query="Summarize this annual report.",

        metadata={

            "file_type": "pdf"

        }

    )

    assert response["success"] is True

    assert "rag" in response["selected_modules"]


@pytest.mark.asyncio
async def test_csv_analysis():

    response = await run_agent(

        query="Analyze this sales dataset.",

        metadata={

            "file_type": "csv"

        }

    )

    assert response["success"] is True

    assert "ml" in response["selected_modules"]


@pytest.mark.asyncio
async def test_image_analysis():

    response = await run_agent(

        query="Extract text from this image.",

        metadata={

            "file_type": "png"

        }

    )

    assert response["success"] is True

    assert "cv" in response["selected_modules"]


@pytest.mark.asyncio
async def test_general_query():

    response = await run_agent(

        query="Hello",

        metadata={}

    )

    assert response["success"] is True

    assert response["intent"] is not None