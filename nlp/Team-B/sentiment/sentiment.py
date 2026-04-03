import json

def get_sentiment(text):

    text = text.lower()

    positive_words = [
        "good", "great", "excellent",
        "amazing", "nice", "worth"
    ]

    negative_words = [
        "bad", "poor", "worst",
        "slow", "disappointing"
    ]

    for word in positive_words:
        if word in text:
            return "positive"

    for word in negative_words:
        if word in text:
            return "negative"

    return "neutral"