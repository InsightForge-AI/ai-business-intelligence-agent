def summarize_text(text):
    if not text or len(text.strip()) == 0:
        return ""

    text = text.strip()

    # If very short → return as is
    if len(text) <= 100:
        return text

    # Split into sentences
    sentences = text.split('.')

    # Return first meaningful sentence
    for sentence in sentences:
        if len(sentence.strip()) > 20:
            return sentence.strip() + "."

    return text[:100]