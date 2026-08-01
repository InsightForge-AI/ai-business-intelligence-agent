"""
==========================================================
Computer Vision Integration Tests
==========================================================

Tests the complete CV pipeline.
"""

import pytest

from services.cv_service import run_analysis


@pytest.mark.asyncio
async def test_cv_pipeline():
    """
    Test complete CV pipeline.
    """

    response = await run_analysis(

        query="Extract invoice details.",

        content="sample_data/invoice.png",

        metadata={

            "file_name": "invoice.png",

            "document_type": "image/png"

        }

    )

    assert response.module == "cv"

    assert response.success is True

    assert isinstance(

        response.document_type,

        str

    )

    assert isinstance(

        response.extracted_text,

        str

    )

    assert isinstance(

        response.fields,

        dict

    )

    assert isinstance(

        response.tables,

        list

    )

    assert isinstance(

        response.charts,

        list

    )

    assert isinstance(

        response.confidence,

        float

    )

    assert 0.0 <= response.confidence <= 1.0

    assert response.message == (

        "Computer Vision analysis completed successfully."

    )