from nlp.teamC.src.preprocessing import clean_text
from nlp.teamC.src.llm import ask_llm


stop_words = {
    "the", "is", "and", "a", "an",
    "to", "of", "in", "on", "for",
    "with", "this", "that", "it"
}


def get_keywords(text):

    try:

        cleaned = clean_text(text)

        if not cleaned:
            return []

        words = cleaned.split()

        keywords = []
        seen = set()

        for word in words:

            if word not in stop_words:

                if word not in seen:

                    keywords.append(word)
                    seen.add(word)

        return keywords

    except Exception:
        return []


def smart_keywords(text):

    try:

        base_keywords = get_keywords(text)

        prompt = f"""
You are a keyword extraction assistant.

Text:
\"\"\"{text}\"\"\"

Initial keywords:
{base_keywords}

Rules:
- Use only words from initial keywords
- Return comma separated keywords only
- No explanation
"""

        llm_result = ask_llm(prompt)

        if llm_result:

            words = [
                w.strip().lower()
                for w in llm_result.split(",")
            ]

            filtered = []

            for word in words:

                if word in base_keywords:

                    if word not in filtered:
                        filtered.append(word)

            if filtered:
                return filtered

        return base_keywords

    except Exception:
        return get_keywords(text)