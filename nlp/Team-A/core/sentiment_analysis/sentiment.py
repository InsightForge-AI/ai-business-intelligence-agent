from app.models.sentiment_bm import get_analyzer

analyzer = get_analyzer()


def get_sentiment(text: str) -> str:
    if not isinstance(text, str):
        return "neutral"

    score = analyzer.polarity_scores(text)
    compound = score['compound']

    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"