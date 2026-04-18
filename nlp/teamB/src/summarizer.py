import re


def preprocess(text):

    if not text or text.strip() == "":
        return None

    cleaned = text.lower()

    # remove symbols except dot
    cleaned = re.sub(r'[^a-z0-9\s\.]', ' ', cleaned)

    cleaned = " ".join(cleaned.split())

    return cleaned


def summarize(text):

    if not text or text.strip() == "":
        return "No text provided"

    clean_original = re.sub(
        r'[^a-zA-Z0-9\s\.]',
        ' ',
        text
    )

    clean_original = " ".join(clean_original.split())

    # Keep cleaned original sentences
    original_sentences = re.split(
        r'\.+\s*',
        clean_original
    )

    original_sentences = [
        s.strip() for s in original_sentences
        if s.strip()
    ]


    cleaned_text = preprocess(text)

    if not cleaned_text:
        return "No text provided"

    cleaned_sentences = cleaned_text.split('.')
    cleaned_sentences = [
        s.strip() for s in cleaned_sentences if s.strip()
    ]

    total_sentences = len(original_sentences)

    if total_sentences == 1:
        return original_sentences[0] + "."

    # Decide summary length dynamically
    if total_sentences <= 2:
        summary_length = 1
    elif total_sentences <= 6:
        summary_length = 3
    elif total_sentences <= 10:
        summary_length = 5
    else:
        summary_length = 6

    stop_words = [
        "the", "is", "and", "but",
        "a", "an", "to", "of",
        "in", "on", "for", "with",
        "at", "by", "this", "that",
        "however", "overall"
    ]

    # Word frequency
    word_freq = {}

    for sentence in cleaned_sentences:

        words = sentence.split()

        for word in words:

            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

    # Score sentences
    sentence_scores = {}

    for i in range(len(cleaned_sentences)):

        words = cleaned_sentences[i].split()

        score = 0

        for word in words:

            if word in word_freq:
                score += word_freq[word]

        # Always give slight importance to first sentence
        if i == 0:
            score += 2

        sentence_scores[i] = score

    # Pick top scored sentences
    top_indexes = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:summary_length]

    # Keep original order
    top_indexes = sorted(top_indexes)

    selected_sentences = [
        original_sentences[i]
        for i in top_indexes
    ]

    return ". ".join(selected_sentences) + "."
