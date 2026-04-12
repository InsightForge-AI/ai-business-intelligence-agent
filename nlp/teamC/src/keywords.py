def extract_keywords(text):
    if not text or len(text.strip()) == 0:
        return []

    # Split text into words
    words = text.strip().split()

    # Return first 5 words as keywords
    return words[:5]