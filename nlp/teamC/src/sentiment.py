def get_sentiment(text):
    if not text or text.strip() == "":
        return "neutral"

    text = text.lower()

    positive_words = [
        "good","great","excellent","amazing","awesome","fast","smooth",
        "strong","reliable","easy","nice","beautiful","comfortable",
        "perfect","best","premium","stylish","impressive","love"
    ]

    negative_words = [
        "bad","poor","slow","late","worst","terrible","issue","problem",
        "error","bug","weak","damaged","crash","lag","difficult",
        "frustrating","disappointing","cheap","overheating"
    ]

    words = text.split()

    pos = sum(word in positive_words for word in words)
    neg = sum(word in negative_words for word in words)

    # mixed condition
    if pos > 0 and neg > 0:
        return "mixed"

    elif pos > neg:
        return "positive"

    elif neg > pos:
        return "negative"

    else:
        return "neutral"