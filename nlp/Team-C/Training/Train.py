import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from preprocessing.preprocessing import clean_text
from sklearn.metrics import accuracy_score
# Load dataset
df = pd.read_csv("data/dataset.csv", encoding='latin-1')

# Preprocess
# Preprocess
df['cleaned_text'] = df['review'].apply(clean_text)

# Features & labels
X = df['cleaned_text']
y = df['sentiment']

# Convert text → numbers
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved!")


y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))