def clean_text(text):
    text = text.lower()
    text = text.strip()
    return text

def split_sentences(text):
    sentences = text.split(".")
    return sentences

def summarize(text):

    text = clean_text(text)

    sentences = split_sentences(text)

    # simple summary → first 2 sentences
    summary = ". ".join(sentences[:2])

    return summary


