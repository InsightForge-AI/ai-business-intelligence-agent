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


# TEST BLOCK
if __name__ == "__main__":

    text = "This product is excellent"

    result = get_sentiment(text)

    print(result)    