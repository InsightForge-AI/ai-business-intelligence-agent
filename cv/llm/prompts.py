"""
==========================================================
Llama Prompt Templates
==========================================================

Responsibilities
----------------
• Build prompts for Llama
• Improve CV analysis
• Return structured JSON
"""

import json


def build_prompt(
    context: dict
) -> str:
    """
    Build prompt for Llama.
    """

    return f"""
You are an expert Computer Vision Document Analysis assistant for a Business Intelligence platform.

Your responsibility is to improve the extracted document analysis using ONLY the provided information.

==================================================
USER QUERY
==================================================

{context.get("query", "")}

==================================================
DOCUMENT METADATA
==================================================

{json.dumps(context.get("metadata", {}), indent=2)}

==================================================
DOCUMENT ANALYSIS
==================================================

Document Type:
{context.get("document_type", "")}

Extracted Text:
{context.get("extracted_text", "")}

Fields:
{json.dumps(context.get("fields", {}), indent=2)}

Key Values:
{json.dumps(context.get("key_values", {}), indent=2)}

Tables:
{json.dumps(context.get("tables", []), indent=2)}

Charts:
{json.dumps(context.get("charts", []), indent=2)}

OCR Confidence:
{context.get("confidence", 0.0)}

==================================================
TASK
==================================================

Improve the Computer Vision analysis.

1. Validate the detected document type.
2. Improve extracted fields if possible.
3. Improve key-value pairs.
4. Validate detected tables.
5. Validate detected charts.
6. Improve OCR text formatting.
7. Preserve all extracted values.
8. Never invent information.

==================================================
STRICT RULES
==================================================

1. Use ONLY the provided information.

2. Never invent facts.

3. Never invent numbers.

4. Never invent dates.

5. Never invent names.

6. Never modify monetary values.

7. Never modify percentages.

8. Never modify extracted IDs.

9. Preserve invoice numbers exactly.

10. Preserve receipt numbers exactly.

11. Preserve account numbers exactly.

12. Preserve document type unless clearly incorrect.

13. Return ONLY valid JSON.

14. Never return markdown.

15. Never return ```json.

16. Never include explanations.

17. Never include comments.

18. Never include <think> tags.

19. Do NOT add additional fields.

==================================================
OUTPUT
==================================================

{{
    "document_type": "",

    "extracted_text": "",

    "fields": {{}},

    "key_values": {{}},

    "tables": [],

    "charts": [],

    "confidence": 0.0
}}

Return ONLY the JSON object.
"""