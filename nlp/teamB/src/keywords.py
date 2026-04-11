def get_keywords(text):

    words = text.split()

    stop_words = ["the", "is", "and", "but"]

    keywords = []

    for word in words:

        word = word.lower().strip(".,")
        
        if word not in stop_words:
            keywords.append(word)

        if len(keywords) == 5:
            break

    return keywords
