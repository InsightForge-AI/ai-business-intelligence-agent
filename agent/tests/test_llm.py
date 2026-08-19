"""
==========================================================
LLM Tests
==========================================================

Tests prompt generation, response parsing,
and LLM service.
"""

from unittest.mock import patch

import pytest

from llm.prompts import build_prompt
from llm.parser import parse_response
from llm.llm_service import detect_intent


# ---------------------------------------------------------
# Prompt Generation
# ---------------------------------------------------------

def test_prompt_generation():

    prompt = build_prompt(

        query="Analyze the sales report.",

        metadata={

            "file_type": "pdf"

        }

    )

    assert isinstance(prompt, str)

    assert "Analyze the sales report." in prompt

    assert "AVAILABLE INTENTS" in prompt


# ---------------------------------------------------------
# JSON Parsing
# ---------------------------------------------------------

def test_parse_valid_json():

    response = """

    {

        "intent":"business_analysis"

    }

    """

    intent = parse_response(response)

    assert intent == "business_analysis"


# ---------------------------------------------------------
# Markdown Parsing
# ---------------------------------------------------------

def test_parse_markdown():

    response = """

    ```json

    {

        "intent":"document_summary"

    }

    ```

    """

    intent = parse_response(response)

    assert intent == "document_summary"


# ---------------------------------------------------------
# Think Tag Parsing
# ---------------------------------------------------------

def test_parse_think_tags():

    response = """

    <think>

    Internal reasoning

    </think>

    {

        "intent":"question_answering"

    }

    """

    intent = parse_response(response)

    assert intent == "question_answering"


# ---------------------------------------------------------
# Invalid Response
# ---------------------------------------------------------

def test_invalid_response():

    response = "Hello World"

    intent = parse_response(response)

    assert intent == "general_query"


# ---------------------------------------------------------
# Empty Response
# ---------------------------------------------------------

def test_empty_response():

    intent = parse_response("")

    assert intent == "general_query"


# ---------------------------------------------------------
# detect_intent() -- Graceful Degradation
# ---------------------------------------------------------
#
# Regression tests for the fix in llm/llm_service.py: detect_intent()
# used to let a Phi-3 connection failure propagate all the way up
# through routing/intent_detector.py -> the API layer as an unhandled
# 500. It now catches any failure and returns "", which
# intent_detector.py's existing `if not intent: return "general_query"`
# already handles correctly.

@pytest.mark.asyncio
async def test_detect_intent_returns_empty_string_when_phi3_unreachable():

    with patch(
        "llm.llm_service.generate",
        side_effect=ConnectionError("Phi-3 unreachable"),
    ):
        intent = await detect_intent(
            query="analyze the sales report",
            metadata={},
        )

    assert intent == ""


@pytest.mark.asyncio
async def test_detect_intent_returns_empty_string_on_prompt_build_failure():

    with patch(
        "llm.llm_service.build_prompt",
        side_effect=ValueError("bad metadata"),
    ):
        intent = await detect_intent(
            query="analyze the sales report",
            metadata={},
        )

    assert intent == ""


@pytest.mark.asyncio
async def test_detect_intent_returns_parsed_intent_on_success():

    with patch(
        "llm.llm_service.generate",
        return_value='{"intent": "business_analysis"}',
    ):
        intent = await detect_intent(
            query="analyze the sales report",
            metadata={},
        )

    assert intent == "business_analysis"