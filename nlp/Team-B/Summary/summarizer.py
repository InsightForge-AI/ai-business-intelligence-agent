from preprocess import clean_text
from utils import split_sentences

def summarize(text):

    text = clean_text(text)

    sentences = split_sentences(text)

    # simple summary → first 2 sentences
    summary = ". ".join(sentences[:2])

    return summary


# test run
if __name__ == "__main__":

    text = """Artificial Intelligence is growing rapidly.
    It is used in healthcare, education and business.
    Many companies are investing in AI."""

    result = summarize(text)

    print("Summary:")
    print(result)