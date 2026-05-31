from modules.sentiment import (
    get_sentiment,
    smart_sentiment
)

from modules.keywords import (
    get_keywords,
    smart_keywords
)

from modules.summarizer import (
    summarize,
    smart_summary
)


def process_text(text):


    # Stable results
    base_sentiment = get_sentiment(text)

    base_keywords = get_keywords(text)

    base_summary = summarize(text)

    # Smart enhancement
    sentiment_result = (
        smart_sentiment(text)
        or base_sentiment
    )

    keywords_result = (
        smart_keywords(text)
        or base_keywords
    )

    summary_result = (
        smart_summary(text)
        or base_summary
    )

    return {
        "sentiment": sentiment_result,
        "summary": summary_result,
        "keywords": keywords_result
    }