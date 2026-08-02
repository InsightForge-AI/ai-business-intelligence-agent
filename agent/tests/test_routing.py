"""
==========================================================
Routing Tests
==========================================================

Tests the routing layer.

Responsibilities
----------------
• Intent Detection
• Module Selection
• Execution Planning
"""

import pytest

from routing.intent_detector import detect_intent
from routing.module_selector import select_modules
from routing.execution_plan import build_execution_plan


# ---------------------------------------------------------
# Intent Detection
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_detect_business_intent():

    intent = await detect_intent(

        query="Analyze the quarterly sales report.",

        metadata={

            "file_type": "pdf"

        }

    )

    assert isinstance(intent, str)


@pytest.mark.asyncio
async def test_detect_summary_intent():

    intent = await detect_intent(

        query="Summarize this annual report.",

        metadata={

            "file_type": "pdf"

        }

    )

    assert isinstance(intent, str)


# ---------------------------------------------------------
# Module Selection
# ---------------------------------------------------------

def test_select_modules_csv():

    modules = select_modules(

        intent="data_analysis",

        metadata={

            "file_type": "csv"

        }

    )

    assert "ml" in modules


def test_select_modules_pdf():

    modules = select_modules(

        intent="document_summary",

        metadata={

            "file_type": "pdf"

        }

    )

    assert "rag" in modules


def test_select_modules_image():

    modules = select_modules(

        intent="document_extraction",

        metadata={

            "file_type": "png"

        }

    )

    assert "cv" in modules


# ---------------------------------------------------------
# Execution Plan
# ---------------------------------------------------------

def test_execution_plan_business():

    plan = build_execution_plan(

        intent="business_analysis",

        selected_modules=[

            "rag",

            "ml",

            "nlp"

        ]

    )

    assert plan == [

        "rag",

        "ml",

        "nlp"

    ]


def test_execution_plan_summary():

    plan = build_execution_plan(

        intent="document_summary",

        selected_modules=[

            "rag",

            "nlp"

        ]

    )

    assert plan == [

        "rag",

        "nlp"

    ]


def test_execution_plan_chart():

    plan = build_execution_plan(

        intent="chart_analysis",

        selected_modules=[

            "cv",

            "ml"

        ]

    )

    assert plan == [

        "cv",

        "ml"

    ]