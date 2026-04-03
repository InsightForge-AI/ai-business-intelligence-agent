import pandas as pd


df = pd.read_csv("data/dataset.csv", encoding='latin-1')

print(df.head())
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)



import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocessing import clean_text

# Train Model


# Preprocess
df['cleaned_text'] = df['review'].apply(clean_text)

# Features & labels
X = df['cleaned_text']
y = df['sentiment']

# Convert text → numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['cleaned_text'])

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved!")


#prediction

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