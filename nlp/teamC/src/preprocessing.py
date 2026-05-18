import re


def clean_text(text):

    if not text:
        return ""

    text = str(text).lower()

    # remove special characters
    text = re.sub(r"[^a-z0-9\s.]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text