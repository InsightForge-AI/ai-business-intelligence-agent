import pickle
from preprocessing.preprocessing import clean_text

# Load model & vectorizer once
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def analyze_sentiment(text):
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]

    return {
        "input": text,
        "cleaned": cleaned,
        "sentiment": prediction.capitalize()
    }