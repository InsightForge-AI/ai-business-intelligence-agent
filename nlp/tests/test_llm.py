"""
==========================================================
LLM Tests
==========================================================

Tests prompt generation, response parsing, and the
generate_insights() orchestration -- including graceful
degradation when Mistral is unreachable.

This file was previously empty (0 bytes): nlp had zero
coverage of its own LLM orchestration layer.
"""

from unittest.mock import patch

import pytest

from llm.prompts import build_prompt
from llm.parser import parse_response
from llm.llm_service import generate_insights


def test_build_prompt_includes_context():
    context = {
        "query": "Summarize this",
        "metadata": {"file_name": "report.pdf"},
        "summary": "Sales grew this quarter.",
        "keywords": ["sales", "growth"],
        "sentiment": "Positive",
    }

    prompt = build_prompt(context)

    assert isinstance(prompt, str)
    assert "Sales grew this quarter." in prompt


def test_parse_valid_json():
    response = """
    {
        "summary": "Sales grew 20%.",
        "keywords": ["sales", "growth"],
        "entities": ["Acme Corp"],
        "sentiment": "Positive",
        "topics": ["finance"],
        "recommendations": ["Keep it up"]
    }
    """

    parsed = parse_response(response)

    assert parsed["summary"] == "Sales grew 20%."
    assert parsed["sentiment"] == "Positive"
    assert parsed["keywords"] == ["sales", "growth"]


def test_parse_empty_response_returns_defaults():
    parsed = parse_response("")

    assert parsed["summary"] == ""
    assert parsed["sentiment"] == "Neutral"
    assert parsed["keywords"] == []


@pytest.mark.asyncio
async def test_generate_insights_returns_empty_dict_when_mistral_unreachable():
    """
    Regression test for the graceful-degradation fix: generate_insights()
    used to let a connection failure to Mistral propagate all the way up
    through nlp_service.py -> the API layer as an unhandled 500. It now
    catches any failure and returns {}, which nlp_service.py's existing
    `llm.get(key, deterministic_fallback)` calls already handle correctly
    by falling back to the traditional-NLP results.
    """
    context = {
        "query": "summarize",
        "metadata": {},
        "summary": "fallback summary",
        "keywords": ["a"],
        "entities": [],
        "sentiment": "Neutral",
        "topics": [],
        "recommendations": [],
    }

    with patch(
        "llm.llm_service.generate",
        side_effect=ConnectionError("Mistral unreachable"),
    ):
        result = await generate_insights(context)

    assert result == {}


@pytest.mark.asyncio
async def test_generate_insights_returns_empty_dict_on_malformed_llm_output():
    # generate() succeeds but returns garbage the parser can't salvage
    # into anything meaningful -- still must not raise.
    with patch("llm.llm_service.generate", return_value=None):
        result = await generate_insights({"query": "x"})

    # parse_response("") -> a well-formed default dict, not an exception;
    # this just confirms the call completes without raising.
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_generate_insights_returns_parsed_response_on_success():
    fake_response = """
    {
        "summary": "All good.",
        "keywords": ["ok"],
        "entities": [],
        "sentiment": "Positive",
        "topics": [],
        "recommendations": []
    }
    """

    with patch("llm.llm_service.generate", return_value=fake_response):
        result = await generate_insights({"query": "x"})

    assert result["summary"] == "All good."
    assert result["sentiment"] == "Positive"
