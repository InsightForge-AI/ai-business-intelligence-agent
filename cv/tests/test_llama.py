"""
==========================================================
Llama Tests
==========================================================

Tests Llama integration.
"""

import pytest

from llm.prompts import build_prompt
from llm.parser import parse_response
from llm.llama import generate


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