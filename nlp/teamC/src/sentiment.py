from nlp.teamC.src.preprocessing import clean_text
from nlp.teamC.src.llm import ask_llm


positive_words = {
    "good", "great", "excellent", "amazing",
    "awesome", "love", "best", "fast",
    "perfect", "nice", "smooth"
}

negative_words = {
    "bad", "worst", "slow", "hate",
    "terrible", "awful", "broken",
    "lag", "poor", "bug"
}


def get_sentiment(text):

    try:

        cleaned = clean_text(text)

        if not cleaned:
            return "neutral"

        words = cleaned.split()

        positive_count = sum(
            1 for word in words
            if word in positive_words
        )

        negative_count = sum(
            1 for word in words
            if word in negative_words
        )

        if positive_count > negative_count:
            return "positive"

        elif negative_count > positive_count:
            return "negative"

        elif positive_count > 0 and negative_count > 0:
            return "mixed"

        return "neutral"

    except Exception:
        return "neutral"


def smart_sentiment(text):

    try:

        base_sentiment = get_sentiment(text)

        prompt = f"""
You are a sentiment classifier.

Text:
\"\"\"{text}\"\"\"

Initial prediction:
{base_sentiment}

Return ONLY one word:
positive
negative
neutral
mixed
"""

        llm_result = ask_llm(prompt)

        allowed = [
            "positive",
            "negative",
            "neutral",
            "mixed"
        ]

        if llm_result:

            llm_result = llm_result.strip().lower()

            if llm_result in allowed:
                return llm_result

        return base_sentiment

    except Exception:
        return get_sentiment(text)