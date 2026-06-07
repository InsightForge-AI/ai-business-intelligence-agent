def sentiment_prompt(text,basic_sentiment):
    return f"""
You are an expert sentiment classifier.

Classify the sentiment of the given text into exactly ONE label:

positive
negative
neutral
mixed

Text:
\"\"\"{text}\"\"\"

Rule-based prediction:
{basic_sentiment}

The rule-based prediction may or may not be correct.
Analyze the text yourself and return the most accurate label.

Rules:
- If both positive and negative opinions are present, return mixed.
- If the overall tone is positive, return positive.
- If the overall tone is negative, return negative.
- If there is no clear sentiment, return neutral.

Return ONLY one word:
positive
negative
neutral
mixed

No explanation.
"""

def summary_prompt(base_summary):
    return f"""
You are an expert business summarization assistant.

Refine the following summary to improve clarity, coherence, readability, and sentence flow.

Rules:
- Preserve all important information.
- Do not add information that is not present.
- Do not remove key business details.
- Remove repetition where appropriate.
- Maintain the original meaning and context.
- Use clear and professional language.
- Ensure important business areas mentioned in the summary remain represented, such as:
  - Financial performance
  - Operations
  - Customer service
  - Product development
  - Risks and challenges
  - Future plans
- Return only the refined summary.

Summary:

{base_summary}
"""

def keyword_prompt(snippet,basic_keywords,chunk_target):
    return f"""
You are a business keyword extraction assistant.

Text snippet:
\"\"\"{snippet}\"\"\"

Candidate keywords:
{basic_keywords}

Rules:
- Select ONLY keywords from the candidate list above. Do NOT add new keywords.
- Pick exactly {chunk_target} most meaningful business-relevant keywords.
- PREFER: nouns (people, departments, metrics, products, places, tools, concepts)
- PREFER: business terms (revenue, profit, sales, hr, workforce, strategy, growth, acquisition, funding, ebitda, crm, saas, okr, attrition, retention, margin, pipeline)
- AVOID: verbs (reached, reflecting, declined, improving, drove, stood)
- AVOID: adjectives (strong, healthy, successful, significant, aggressive)
- AVOID: vague words (team, unit, process, activity, area)
- AVOID: single letters or partial words (s, b, re)
- Return as a comma-separated list only.
- No sentences. No explanations. No numbering.
"""

def recommendation_prompt(
        text,sentiment,keywords,basic_text):
    return f"""
You are an experienced business consultant.

Analyze the provided text and generate exactly 3 recommendations.

Rules:
- Recommendations must be based ONLY on the provided text.
- Do not invent information that is not mentioned in the text.
- Focus on improvement opportunities and business impact.
- Keep recommendations practical and actionable and concise.
- Return only recommendations.
- One recommendation per line.
- No numbering.
- No bullets.
- No labels.

Text:
\"\"\"{text}\"\"\"

Sentiment:
{sentiment}

Keywords:
{keywords}

Existing Recommendations:
{basic_text}
"""
