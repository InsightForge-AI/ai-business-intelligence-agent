"""
==========================================================
LLM Tests
==========================================================

Tests prompt generation, response parsing,
and LLM service.
"""

import pytest

from llm.prompts import build_prompt
from llm.parser import parse_response


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