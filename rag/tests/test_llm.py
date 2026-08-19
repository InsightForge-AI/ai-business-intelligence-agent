"""
==========================================================
LLM Tests
==========================================================

Tests prompt generation, response parsing, and the
generate_answer() orchestration -- including graceful
degradation when Qwen is unreachable.

This file was previously empty (0 bytes): rag had zero
coverage of its own LLM orchestration layer, even though
generate_answer() already has (correct) try/except
handling -- this is what confirmed it actually works.
"""

from unittest.mock import patch

import pytest

from llm.prompts import build_prompt
from llm.parser import parse_response
from llm.llm_service import generate_answer


def test_build_prompt_includes_query_and_context():
    context = {
        "query": "What caused the sales increase?",
        "metadata": {"file_name": "report.pdf"},
        "context": "Sales grew due to a new referral program.",
    }

    prompt = build_prompt(context)

    assert "What caused the sales increase?" in prompt
    assert "Sales grew due to a new referral program." in prompt


def test_parse_valid_json():
    response = '{"answer": "Sales grew due to referrals.", "confidence": 0.9}'

    parsed = parse_response(response)

    assert parsed["answer"] == "Sales grew due to referrals."
    assert parsed["confidence"] == 0.9


def test_parse_confidence_is_clamped_to_valid_range():
    response = '{"answer": "x", "confidence": 5.0}'
    assert parse_response(response)["confidence"] == 1.0

    response = '{"answer": "x", "confidence": -2.0}'
    assert parse_response(response)["confidence"] == 0.0


def test_parse_empty_response_returns_default_answer():
    parsed = parse_response("")
    assert "could not find" in parsed["answer"].lower()
    assert parsed["confidence"] == 0.0


@pytest.mark.asyncio
async def test_generate_answer_with_no_context_short_circuits():
    # No LLM call should happen at all when there's nothing to ground on.
    with patch("llm.llm_service.generate") as mock_generate:
        result = await generate_answer({"query": "what is this?", "context": ""})

    mock_generate.assert_not_called()
    assert result["confidence"] == 0.0


@pytest.mark.asyncio
async def test_generate_answer_returns_safe_default_when_qwen_unreachable():
    """
    Confirms generate_answer()'s existing try/except around the Qwen call
    actually works: a connection failure must not raise past this
    function, unlike agent/nlp/cv's llm_service.py before their fix.
    """
    context = {
        "query": "what caused the increase",
        "context": "Sales grew due to referrals.",
    }

    with patch(
        "llm.llm_service.generate",
        side_effect=ConnectionError("Qwen unreachable"),
    ):
        result = await generate_answer(context)

    assert result["confidence"] == 0.0
    assert "unable to generate" in result["answer"].lower()


@pytest.mark.asyncio
async def test_generate_answer_returns_safe_default_on_unparseable_output():
    context = {"query": "x", "context": "some context"}

    with patch("llm.llm_service.generate", return_value="not json at all {{{"):
        result = await generate_answer(context)

    # parse_response's own except-branch treats unparseable text as a
    # low-confidence literal answer rather than raising, so this must
    # not error either way -- just confirm the call completes cleanly.
    assert "answer" in result and "confidence" in result


@pytest.mark.asyncio
async def test_generate_answer_returns_parsed_response_on_success():
    fake_response = '{"answer": "Referrals drove growth.", "confidence": 0.95}'

    with patch("llm.llm_service.generate", return_value=fake_response):
        result = await generate_answer(
            {"query": "why did sales grow", "context": "referral program"}
        )

    assert result["answer"] == "Referrals drove growth."
    assert result["confidence"] == 0.95
