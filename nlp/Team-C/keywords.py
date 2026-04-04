import pickle
import numpy as np
from preprocessing import clean_text

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

IGNORE_WORDS = {"very", "really", "extremely", "much", "many", "more", "most"}

def extract_keywords(text, top_n=5):
    cleaned_text = clean_text(text)
    tfidf_matrix = vectorizer.transform([cleaned_text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    top_indices = np.argsort(scores)[::-1]

    keywords = []
    seen = set()

    for i in top_indices:
        word = feature_names[i]
        score = scores[i]

        if (
            score > 0.05 and
            len(word) > 4 and
            word not in IGNORE_WORDS and
            word not in seen
        ):
            keywords.append(word)
            seen.add(word)

        if len(keywords) == top_n:
            break

    return keywords