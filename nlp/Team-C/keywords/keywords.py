import re
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stop_words = set(stopwords.words("english"))


def extract_keywords(text, top_n=5):
    if not text or len(text.strip()) == 0:
        return []


    text = re.sub(r"\s+", " ", text.lower())

    
    words = word_tokenize(text)


    filtered_words = [
        word for word in words
        if word.isalnum() and word not in stop_words
    ]

    if not filtered_words:
        return []


    word_freq = Counter(filtered_words)
    keywords = [word for word, freq in word_freq.most_common(top_n)]

    return keywords