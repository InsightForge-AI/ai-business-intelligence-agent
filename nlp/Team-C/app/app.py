
from fastapi import FastAPI
from pydantic import BaseModel
from sentiment.sentiment import analyze_sentiment

# ✅ MUST be at top-level (not inside any function)
app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is running 🚀"}

@app.post("/predict")
def predict(data: TextInput):
    result = analyze_sentiment(data.text)
    return result