"""
==========================================================
Llama Tests
==========================================================

Tests Llama integration.
"""

from unittest.mock import patch

import pytest

from llm.prompts import build_prompt
from llm.parser import parse_response
from llm.llama import generate
from llm.llm_service import generate_insights


def test_build_prompt():
    """
    Test prompt generation.
    """

    context = {

        "query": "Extract invoice details.",

        "metadata": {

            "file_name": "invoice.png"

        },

        "document_type": "Invoice",

        "extracted_text": "Invoice Number: INV-1001",

        "fields": {

            "invoice_number": "INV-1001"

        },

        "key_values": {

            "vendor": "ABC Corporation"

        },

        "tables": [],

        "charts": [],

        "confidence": 0.95

    }

    prompt = build_prompt(

        context

    )

    assert "Invoice" in prompt

    assert "INV-1001" in prompt

    assert "ABC Corporation" in prompt


def test_parser():
    """
    Test JSON parser.
    """

    response = """
    {
        "document_type":"Invoice",
        "extracted_text":"Invoice Number: INV-1001",
        "fields":{
            "invoice_number":"INV-1001"
        },
        "key_values":{
            "vendor":"ABC Corporation"
        },
        "tables":[],
        "charts":[],
        "confidence":0.96
    }
    """

    parsed = parse_response(

        response

    )

    assert parsed["document_type"] == "Invoice"

    assert parsed["fields"]["invoice_number"] == "INV-1001"

    assert parsed["confidence"] == 0.96


@pytest.mark.asyncio
async def test_llama():
    """
    Test Ollama Llama.
    """

    prompt = """

    Return ONLY JSON.

    {
        "document_type":"Invoice",
        "extracted_text":"Invoice Number: INV-1001",
        "fields":{
            "invoice_number":"INV-1001"
        },
        "key_values":{},
        "tables":[],
        "charts":[],
        "confidence":1.0
    }

    """

    response = await generate(

        prompt

    )

    assert isinstance(

        response,

        str

    )

    assert len(

        response

    ) > 0


# ---------------------------------------------------------
# generate_insights() -- Graceful Degradation
# ---------------------------------------------------------
#
# Regression tests for the fix in llm/llm_service.py: generate_insights()
# used to let a Llama connection failure propagate all the way up through
# cv_service.py -> the API layer as an unhandled 500. It now catches any
# failure and returns {}, which cv_service.py's existing
# `llm.get(key, deterministic_fallback)` calls already handle correctly
# by falling back to the OCR/extraction results.

@pytest.mark.asyncio
async def test_generate_insights_returns_empty_dict_when_llama_unreachable():

    context = {
        "query": "extract invoice details",
        "metadata": {},
        "document_type": "Invoice",
        "extracted_text": "Invoice Number: INV-1001",
        "fields": {},
        "key_values": {},
        "tables": [],
        "charts": [],
        "confidence": 0.9,
    }

    with patch(
        "llm.llm_service.generate",
        side_effect=ConnectionError("Llama unreachable"),
    ):
        result = await generate_insights(context)

    assert result == {}


@pytest.mark.asyncio
async def test_generate_insights_returns_parsed_response_on_success():

    fake_response = """
    {
        "document_type": "Invoice",
        "extracted_text": "Invoice Number: INV-1001",
        "fields": {"invoice_number": "INV-1001"},
        "key_values": {},
        "tables": [],
        "charts": [],
        "confidence": 0.97
    }
    """

    with patch("llm.llm_service.generate", return_value=fake_response):
        result = await generate_insights({"query": "x"})

    assert result["document_type"] == "Invoice"
    assert result["confidence"] == 0.97