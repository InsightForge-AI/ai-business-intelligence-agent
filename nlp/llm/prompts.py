"""
==========================================================
Mistral Prompt Templates
==========================================================

Responsibilities
----------------
• Improve deterministic NLP results
• Never invent information
• Return consistent JSON
"""

import json


def build_prompt(context: dict) -> str:
    """
    Build prompt for Mistral.
    """

    return f"""
You are an expert Natural Language Processing Analyst working for a
Business Intelligence platform.

Your job is to improve an existing NLP analysis.

You MUST use ONLY the information provided below.

==================================================
USER QUERY
==================================================

{context.get("query", "")}

==================================================
DOCUMENT METADATA
==================================================

{json.dumps(context.get("metadata", {}), indent=2)}

==================================================
CURRENT NLP ANALYSIS
==================================================

Summary
-------
{context.get("summary", "")}

Keywords
--------
{json.dumps(context.get("keywords", []), indent=2)}

Entities
--------
{json.dumps(context.get("entities", []), indent=2)}

Sentiment
---------
{context.get("sentiment", "")}

Topics
------
{json.dumps(context.get("topics", []), indent=2)}

Recommendations
---------------
{json.dumps(context.get("recommendations", []), indent=2)}

==================================================
YOUR TASK
==================================================

Improve the NLP analysis while preserving factual accuracy.

1. Rewrite the summary into a concise executive summary.

2. Improve the keywords.

   • Keep only meaningful business keywords.

   • Remove generic words.

   • Prefer business phrases.

3. Improve the entities.

   ONLY include:

   • Organizations

   • People

   • Locations

   • Dates

   • Monetary values

   • Percentages

   • Products

   Do NOT include:

   • File names

   • Document types

   • Generic nouns

4. Validate the sentiment.

   Allowed values ONLY:

   Positive

   Neutral

   Negative

   Mixed

5. Improve the topics.

   Use concise business topics.

6. Improve the recommendations.

   Recommendations MUST be directly based on the document.

   Never generate generic recommendations.

   Each recommendation must be actionable.

==================================================
STRICT RULES
==================================================

1. Respond ONLY in English.

2. Use ONLY the supplied information.

3. Never invent facts.

4. Never invent entities.

5. Never invent numbers.

6. Never change numerical values.

7. Never use Markdown.

8. Never use ```json.

9. Never include explanations.

10. Never include comments.

11. Never include <think> tags.

12. Never add extra fields.

13. Remove duplicate keywords.

14. Remove duplicate entities.

15. Return at most:

• 8 keywords

• 8 entities

• 3 topics

• 3 recommendations

16. Every array element must be a string.

17. Summary must be a single paragraph.

18. Return ONLY valid JSON.

==================================================
OUTPUT
==================================================

{{
  "summary": "",

  "keywords": [],

  "entities": [],

  "sentiment": "",

  "topics": [],

  "recommendations": []
}}

Return ONLY the JSON object.
"""