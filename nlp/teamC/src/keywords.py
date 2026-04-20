def get_keywords(text):

    # Preprocessing
    if text is None:
        return ["No keywords found"]

    text = str(text)

    # lowercase
    text = text.lower()

    # remove special characters
    import re
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Handle empty input
    if not text:
        return ["No keywords found"]

    words = text.split()

    stop_words = [
        "the","this","that","it", "is", "and", "but","i","am","i'm",
        "a", "an", "to", "of","or","was",
        "in", "on", "for", "with","are", "be", "by", "as", "at", "from","since"
          ]

    keywords = []
    seen = set()

    for word in words:

        if word not in stop_words:

            # Remove duplicates
            if word not in seen:
                keywords.append(word)
                seen.add(word)



    if len(keywords) == 0:
            return ["No keywords found"]

    return keywords
