"""
==========================================================
Phi-3 Prompt Templates
==========================================================

Responsibilities
----------------
• Build prompts for Phi-3
• Detect user intent
"""

import json


def build_prompt(
    query: str,
    metadata: dict
) -> str:
    """
    Build prompt for intent detection.
    """

    return f"""
You are an AI Routing Agent.

Your job is to classify the user's request into ONE intent.

==================================================
USER QUERY
==================================================

{query}

==================================================
DOCUMENT METADATA
==================================================

{json.dumps(metadata, indent=2)}

==================================================
AVAILABLE INTENTS
==================================================

business_analysis
document_summary
question_answering
data_analysis
document_extraction
chart_analysis
general_query

==================================================
INTENT DEFINITIONS
==================================================

business_analysis
- Analyze business reports
- Sales analysis
- Profit analysis
- Revenue analysis
- KPI analysis
- Financial performance

document_summary
- Summarize documents
- Generate executive summaries
- Shorten reports

question_answering
- Answer questions from a document
- Find specific information
- Retrieve facts

data_analysis
- Analyze CSV
- Analyze Excel
- Dataset analysis
- Statistics

document_extraction
- OCR
- Extract text
- Extract tables
- Extract key fields
- Read invoices
- Read forms

chart_analysis
- Analyze graphs
- Analyze charts
- Analyze diagrams
- Visual analytics

general_query
- Greetings
- General conversation
- Unknown requests

==================================================
RULES
==================================================

1. Choose ONLY ONE intent.

2. Return ONLY valid JSON.

3. Do NOT explain.

4. Do NOT use Markdown.

5. Do NOT use <think> tags.

6. Do NOT create additional fields.

==================================================
OUTPUT
==================================================

{{
    "intent": ""
}}

Return ONLY the JSON object.
"""