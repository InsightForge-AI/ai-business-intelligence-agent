import re

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # remove special chars
    return text.strip()

def get_sentiment(text):
    text = clean_text(text)

    if not text:
        return "neutral"

    words = text.split()

    positive_words = {"good", "great", "excellent", "happy", "love", "awesome"}
    negative_words = {"bad", "terrible", "sad", "hate", "worst", "poor"}

    pos_count = sum(1 for word in words if word in positive_words)
    neg_count = sum(1 for word in words if word in negative_words)

    # Mixed sentiment handling
    if pos_count > 0 and neg_count > 0:
        return "mixed"
    elif pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"