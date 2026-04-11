def get_sentiment(text):
    if not text or len(text.strip()) == 0:
        return "neutral"

    text = text.lower()

    positive_words = ["good", "great", "excellent", "happy", "love", "awesome"]
    negative_words = ["bad", "terrible", "sad", "hate", "worst", "poor"]

    # Check for positive words
    for word in positive_words:
        if word in text:
            return "positive"

    # Check for negative words
    for word in negative_words:
        if word in text:
            return "negative"

    return "neutral"