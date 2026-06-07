from modules.sentiment import (
    get_sentiment,
    smart_sentiment
)

from modules.keywords import (
    get_keywords,
    smart_keywords
)

from modules.summarizer import (
    get_summary,
    smart_summary
)

from modules.recommendations import(
    get_recommendations,
    smart_recommendations
)

def should_generate_recommendations(text, keywords):

    if not text or not str(text).strip():
        return False

    if not keywords:
        return False

    if keywords == ["No keywords found"]:
        return False

    words = str(text).split()

    # Too short to generate useful recommendations
    if len(words) < 3:
        return False

    # At least one keyword should contain letters
    valid_keywords = [
        k for k in keywords
        if any(ch.isalpha() for ch in str(k))
    ]

    if not valid_keywords:
        return False

    return True

def process_text(text):

    base_sentiment = get_sentiment(text)

    base_keywords = get_keywords(text)

    base_summary = get_summary(text)

    base_recommendations = get_recommendations(
        text,
        base_sentiment,
        base_keywords
    )

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


    if should_generate_recommendations(
            text,
            keywords_result
    ):

        recommendations_result = (
            smart_recommendations(
                text,
                sentiment_result,
                keywords_result
            )
            or base_recommendations
        )

    else:
        recommendations_result = []

       

  

    return {
        "sentiment": sentiment_result,
        "summary": summary_result,
        "keywords": keywords_result,
        "recommendations": recommendations_result
    }