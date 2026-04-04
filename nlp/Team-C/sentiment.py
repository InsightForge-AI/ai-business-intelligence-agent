import joblib
import os
from preprocessing import clean_text

# Get correct absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load model safely
try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")
    model = None
    vectorizer = None


def get_sentiment(text):
    if model is None or vectorizer is None:
        return "Model not loaded"

    if not text:
        return "Invalid input"

    # 1. Preprocess
    cleaned_text = clean_text(text)

    # 2. Vectorize
    vectorized_text = vectorizer.transform([cleaned_text])

    # 3. Predict
    prediction = model.predict(vectorized_text)

    return prediction[0]