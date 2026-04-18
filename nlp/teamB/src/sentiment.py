import re


def preprocess_text(text):
    
    if not text or not str(text).strip():
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # remove symbols
    text = re.sub(r"\s+", " ", text).strip()   # remove extra spaces
    return text


def get_sentiment(text):
   
    text = preprocess_text(text)

    if not text:
        return "neutral"

    positive_words = {
      "good", "great", "excellent", "amazing", "nice", "worth", "fast", "love", "awesome", "fantastic", "perfect", "best", "wonderful", "superb", "brilliant", "outstanding", 
      "cool", "happy", "satisfied", "pleasant", "impressive", "reliable", "smooth", "easy", "helpful", "beautiful", "strong", "smart", "recommend", "premium", "quality", 
      "valuable", "efficient", "quick", "positive", "enjoy", "liked", "favorite", "delightful","super","fine","recommended"}

    negative_words = {
      "bad", "poor", "worst", "slow", "disappointing", "late", "hate", "awful", "terrible", "horrible", "useless", "waste", "broken", "cheap", "weak", "boring", "annoying", "hard",
      "difficult", "problem", "issue", "error", "bug", "lag", "delay", "negative", "frustrating", "dirty", "ugly", "noisy",
      "expensive", "overpriced", "damaged", "unreliable", "fail", "failed", "poorly", "dislike", "regret", "pathetic", "mess"}

    words = text.split()

    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    if "not soo" in text:
        return "neutral"
    elif positive_count > 0 and negative_count > 0:
        return "mixed"
    elif positive_count > negative_count:
        if "not" in words:
            return "negative"
        return "positive"
    elif negative_count > positive_count:
        if "not" in words:
            return "positive"
        return "negative"
    else:
        return "neutral"

