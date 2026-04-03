import pickle
from preprocessing import clean_text

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_sentiment(text):
    text = clean_text(text)
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]

    return "Positive" if prediction == 1 else "Negative"


if __name__ == "__main__":
    text = input("Enter text: ")
    print(predict_sentiment(text))