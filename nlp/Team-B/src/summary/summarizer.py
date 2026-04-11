from .preprocess import clean_text
from .utils import split_sentences

def summarize(text):

    text = clean_text(text)

    sentences = split_sentences(text)

    # simple summary → first 2 sentences
    summary = ". ".join(sentences[:2])

    return summary


